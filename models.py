from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

# Junction tables
player_campaign = db.Table('player_campaign',
    db.Column('player_id', db.String, db.ForeignKey('players.player_id'), primary_key=True),
    db.Column('campaign_id', db.String, db.ForeignKey('campaigns.campaign_id'), primary_key=True)
)

player_device = db.Table('player_device',
    db.Column('player_id', db.String, db.ForeignKey('players.player_id'), primary_key=True),
    db.Column('device_id', db.Integer, db.ForeignKey('devices.id'), primary_key=True)
)

player_item = db.Table('player_item',
    db.Column('player_id', db.String, db.ForeignKey('players.player_id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('items.id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False, default=1)
)

class Player(db.Model):
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
    items = db.relationship('Item', secondary=player_item, lazy='subquery',
                           backref=db.backref('players', lazy=True))
    campaigns = db.relationship('Campaign', secondary=player_campaign, lazy='subquery',
                               backref=db.backref('players', lazy=True))
    clan = db.relationship('Clan', backref='players')
    
    def to_dict(self):
        """Convert player object to dictionary for JSON response"""
        # Get inventory with quantities
        inventory_dict = {}
        for item_association in db.session.query(player_item).filter_by(player_id=self.player_id).all():
            item = Item.query.get(item_association.item_id)
            inventory_dict[item.key] = item_association.quantity
        
        active_campaigns = [campaign.name for campaign in self.campaigns]
        
        clan_dict = None
        if self.clan:
            clan_dict = {
                "id": self.clan.clan_id,
                "name": self.clan.name
            }
        
        devices_list = []
        for device in self.devices:
            devices_list.append({
                "id": device.device_id,
                "model": device.model,
                "carrier": device.carrier,
                "firmware": device.firmware
            })
            
        return {
            "player_id": self.player_id,
            "credential": self.credential,
            "created": self.created.strftime("%Y-%m-%d %H:%M:%SZ") if self.created else None,
            "modified": self.modified.strftime("%Y-%m-%d %H:%M:%SZ") if self.modified else None,
            "last_session": self.last_session.strftime("%Y-%m-%d %H:%M:%SZ") if self.last_session else None,
            "total_spent": self.total_spent,
            "total_refund": self.total_refund,
            "total_transactions": self.total_transactions,
            "last_purchase": self.last_purchase.strftime("%Y-%m-%d %H:%M:%SZ") if self.last_purchase else None,
            "active_campaigns": active_campaigns,
            "devices": devices_list,
            "level": self.level,
            "xp": self.xp,
            "total_playtime": self.total_playtime,
            "country": self.country,
            "language": self.language,
            "birthdate": self.birthdate.strftime("%Y-%m-%d %H:%M:%SZ") if self.birthdate else None,
            "gender": self.gender,
            "inventory": inventory_dict,
            "clan": clan_dict,
            "_customfield": self.custom_field
        }


class Clan(db.Model):
    __tablename__ = 'clans'
    
    clan_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)


class Device(db.Model):
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, nullable=False)
    model = db.Column(db.String)
    carrier = db.Column(db.String)
    firmware = db.Column(db.String)
    
    __table_args__ = (
        db.UniqueConstraint('device_id', 'model', name='uix_device_id_model'),
    )


class Item(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String)
    description = db.Column(db.String)
    

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    
    def get_matchers(self):
        """
        This is a mock method since we're not storing matchers in the database.
        In a real application, this would retrieve the data from the database.
        """
        return {}
    
    def to_dict(self):
        """Convert campaign object to dictionary"""
        return {
            "id": self.campaign_id,
            "name": self.name
        }