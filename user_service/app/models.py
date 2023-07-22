#app/models.py

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f"<User {self.username}>"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_access_token(self):
        return create_access_token(identity=self.id)  # Use the user's ID as the identity

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()
