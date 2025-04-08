"""
Item model
"""
from . import db


class Item(db.Model):
    """Item model representing in-game items"""
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String)
    description = db.Column(db.String)
