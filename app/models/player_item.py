"""
PlayerItem association model between Player and Item
"""
from . import db


class PlayerItem(db.Model):
    """Association model between Player and Item with quantity"""
    __tablename__ = 'player_item'

    player_id = db.Column(
        db.String,
        db.ForeignKey('players.player_id'),
        primary_key=True)
    item_id = db.Column(
        db.Integer,
        db.ForeignKey('items.id'),
        primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # Relationship to Item
    item = db.relationship("Item")
