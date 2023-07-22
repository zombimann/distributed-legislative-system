#app/__init__.py

from flask import Flask

app = Flask(__name__)

# Load the configuration from config.py
app.config.from_pyfile('../config.py')

# Set the environment to "testing" during testing
if app.config.get('ENV') == 'testing':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# Initialize the database
from app.models import db
db.init_app(app)
