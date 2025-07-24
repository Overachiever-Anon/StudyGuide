import os
from flask import Flask, jsonify
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": os.environ.get('FRONTEND_URL')}}, supports_credentials=True)

    # App Configuration
    app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions within the app factory
    from .extensions import db, bcrypt
    db.init_app(app)
    bcrypt.init_app(app)

    # Register Blueprints
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

    # Register CLI commands
    from .cli import register_cli_commands
    register_cli_commands(app)

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the EduForge API!"})

    return app
