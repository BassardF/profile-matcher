"""
Serialization schemas package
"""
from flask_marshmallow import Marshmallow

ma = Marshmallow()

# Import schemas to make them available when importing the package
from .player import PlayerSchema, player_schema, players_schema
from .item import ItemSchema, item_schema, items_schema
from .device import DeviceSchema, device_schema, devices_schema
from .campaign import CampaignSchema, campaign_schema, campaigns_schema
from .clan import ClanSchema
from .matcher import MatcherSchema, APICampaignSchema, api_campaign_schema, api_campaigns_schema
