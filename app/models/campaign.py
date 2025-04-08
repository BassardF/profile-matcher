"""
Campaign model
"""
from . import db


class Campaign(db.Model):
    """Campaign model representing marketing campaigns"""
    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
