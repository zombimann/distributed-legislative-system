# app/__init__.py

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Add this import
from config import Config, TestConfig

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate extension

api = Api(app)

from app import routes, models

# Register the resources after importing routes
api.add_resource(routes.AmendmentListResource, '/api/amendments')
api.add_resource(routes.AmendmentResource, '/api/amendments/<int:amendment_id>')
