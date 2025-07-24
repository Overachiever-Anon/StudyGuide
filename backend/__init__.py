import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

def create_app():
    """Creates and configures the Flask application."""
    load_dotenv()

    app = Flask(__name__)

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
    frontend_url = os.environ.get('FRONTEND_URL')
    if frontend_url:
        CORS(app, resources={r"/api/*": {"origins": frontend_url}}, supports_credentials=True)
    else:
        CORS(app, supports_credentials=True) # Fallback for local development

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

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the EduForge API!"})

    return app
