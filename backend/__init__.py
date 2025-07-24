import os
import sys
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

def create_app():
    """Creates and configures the Flask application."""
    load_dotenv()

    # Determine if we're using the static folder from Docker (production) or local development
    static_folder = os.path.join(os.path.dirname(__file__), 'static')
    if os.path.exists(static_folder):
        # In production/Docker, serve frontend files from the static folder
        app = Flask(__name__, static_folder=static_folder)
        print(f"Using static folder: {static_folder}", file=sys.stderr)
    else:
        # In development, don't use a static folder as the frontend is served by Vite
        app = Flask(__name__)
        print("No static folder found, running in development mode", file=sys.stderr)
    
    # --- App Configuration ---
    app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Validation ---
    if not app.config['SECRET_KEY']:
        raise ValueError("A JWT_SECRET_KEY is required.")
    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise ValueError("A DATABASE_URL is required.")

    # --- CORS Configuration ---
    # In production, no need for CORS as frontend and backend are served from same origin
    # But keep it for development where they might be on different ports
    CORS(app, supports_credentials=True)

    # --- Initialize Extensions ---
    from .extensions import db, bcrypt, migrate, init_supabase
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db) # For database migrations
    init_supabase() # For Supabase file storage

    # --- Register Blueprints ---
    from .routes.auth import auth_bp
    from .routes.upload import upload_bp
    from .routes.lectures import lectures_bp
    from .routes.exams import exams_bp
    from .routes.ai import ai_bp
    from .routes.artifacts import artifacts_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(upload_bp, url_prefix='/api')
    app.register_blueprint(lectures_bp, url_prefix='/api')
    app.register_blueprint(exams_bp, url_prefix='/api')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(artifacts_bp, url_prefix='/api/artifacts')

    # --- Register CLI Commands ---
    from .cli import register_cli_commands
    register_cli_commands(app)

    # Serve React App - catch all route to serve index.html for client-side routing
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        # If the path is an API route, let Flask handle it normally
        if path.startswith('api/'):
            return app.send_static_file('index.html')
        
        # For all frontend routes, serve the index.html file from the static folder
        try:
            if path and os.path.exists(os.path.join(app.static_folder, path)):
                return send_from_directory(app.static_folder, path)
            return send_from_directory(app.static_folder, 'index.html')
        except:
            # If in development mode without static files, return API welcome message
            if not app.static_folder or not os.path.exists(app.static_folder):
                return jsonify({"message": "Welcome to the EduForge API!"})
            return app.send_static_file('index.html')

    return app
