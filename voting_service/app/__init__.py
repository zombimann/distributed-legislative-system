# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate  # Import the Migrate class

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()  # Initialize the Migrate object

def create_app():
    app = Flask(__name__)

    # Load configuration from the config.py file
    app.config.from_object('config')

    # Initialize database and JWT
    db.init_app(app)
    jwt.init_app(app)

    # Import and register blueprints
    from app.routes import voting_bp
    app.register_blueprint(voting_bp)

    return app

