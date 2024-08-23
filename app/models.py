# models.py

from app import db


class TechStack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    popularity = db.Column(db.Float)


class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tech_stack_id = db.Column(
        db.Integer, db.ForeignKey("tech_stack.id"), nullable=False
    )
    recommendation = db.Column(db.Text, nullable=False)
    reason = db.Column(db.Text)
    score = db.Column(db.Float)
