#app/model.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CommitteeMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    nomination_status = db.Column(db.Boolean, default=False)
    elected_status = db.Column(db.Boolean, default=False)
