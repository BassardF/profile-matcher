"""
Player model and related association tables
"""
from . import db
from typing import List, Dict
from .player_item import PlayerItem

# Association tables
player_campaign = db.Table('player_campaign',
    db.Column('player_id', db.String, db.ForeignKey('players.player_id'), primary_key=True),
    db.Column('campaign_id', db.String, db.ForeignKey('campaigns.campaign_id'), primary_key=True)
)

player_device = db.Table('player_device',
    db.Column('player_id', db.String, db.ForeignKey('players.player_id'), primary_key=True),
    db.Column('device_id', db.Integer, db.ForeignKey('devices.id'), primary_key=True)
)

class Player(db.Model):
    """Player model representing user profiles"""
    __tablename__ = 'players'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_id = db.Column(db.String, unique=True, nullable=False)
    credential = db.Column(db.String)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    last_session = db.Column(db.DateTime)
    total_spent = db.Column(db.Float)
    total_refund = db.Column(db.Float)
    total_transactions = db.Column(db.Integer)
    last_purchase = db.Column(db.DateTime)
    level = db.Column(db.Integer)
    xp = db.Column(db.Integer)
    total_playtime = db.Column(db.Integer)
    country = db.Column(db.String)
    language = db.Column(db.String)
    birthdate = db.Column(db.DateTime)
    gender = db.Column(db.String)
    clan_id = db.Column(db.String, db.ForeignKey('clans.clan_id'))
    custom_field = db.Column(db.String)
    
    # Relationships
    devices = db.relationship('Device', secondary=player_device, lazy='subquery',
                             backref=db.backref('players', lazy=True))
    inventory = db.relationship('PlayerItem', lazy='subquery',
                                cascade='all, delete-orphan',
                                backref=db.backref('player', lazy=True))
    campaigns = db.relationship('Campaign', secondary=player_campaign, lazy='subquery',
                               backref=db.backref('players', lazy=True))
    clan = db.relationship('Clan', backref='players')
    
    def get_items_dict(self) -> Dict[str, int]:
        """Convert player items to a dictionary mapping item keys to quantities"""
        result = {}
        for player_item in self.inventory:
            if player_item.item:
                result[player_item.item.key] = player_item.quantity
        return result
    
    def get_item_names(self) -> List[str]:
        """Get a list of item names that the player has with quantity > 0
        
        Returns:
            List[str]: List of item names
        """
        return [player_item.item.name for player_item in self.inventory 
                if player_item.item and player_item.quantity > 0]
    
    def has_all_items(self, item_names: List[str]) -> bool:
        """Check if player has all the specified items with quantity > 0
        
        Args:
            item_names: List of item names to check
            
        Returns:
            bool: True if player has all items, False otherwise
        """
        player_items = self.get_item_names()
        return all(item in player_items for item in item_names)
    
    def has_any_items(self, item_names: List[str]) -> bool:
        """Check if player has any of the specified items with quantity > 0
        
        Args:
            item_names: List of item names to check
            
        Returns:
            bool: True if player has any of the items, False otherwise
        """
        player_items = self.get_item_names()
        return any(item in player_items for item in item_names)
        
    def has_campaign(self, campaign_id: str) -> bool:
        """Check if player is already assigned to a campaign
        
        Args:
            campaign_id: The ID of the campaign to check
            
        Returns:
            bool: True if player is already assigned to the campaign, False otherwise
        """
        return any(campaign_id == campaign.campaign_id for campaign in self.campaigns)