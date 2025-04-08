"""
Database models package
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models to make them available when importing the package
from .player import Player, player_campaign, player_device
from .player_item import PlayerItem
from .item import Item
from .device import Device
from .campaign import Campaign
from .clan import Clan
