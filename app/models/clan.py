"""
Clan model
"""
from . import db

class Clan(db.Model):
    """Clan model representing player groups"""
    __tablename__ = 'clans'
    
    clan_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
