# app/models.py
from app import db

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(200))
    author_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Bill {self.title}>"
