# config.py
import os

class Config:
    DEBUG = True
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql://zombi:C0mpradors*@localhost/amendment_service_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use an in-memory SQLite database for testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_test_secret_key'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
