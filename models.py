from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    
    devices = db.relationship('Device', secondary=player_device, lazy='subquery',
                             backref=db.backref('players', lazy=True))
    items = db.relationship('Item', secondary=player_item, lazy='subquery',
                           backref=db.backref('players', lazy=True))
    campaigns = db.relationship('Campaign', secondary=player_campaign, lazy='subquery',
                               backref=db.backref('players', lazy=True))
    clan = db.relationship('Clan', backref='players')


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