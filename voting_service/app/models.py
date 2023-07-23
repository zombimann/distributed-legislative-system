# app/models.py

from app import db

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    tags = db.Column(db.String(255), nullable=True)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    bill_id = db.Column(db.Integer, nullable=False)
    vote = db.Column(db.Boolean, nullable=False)
