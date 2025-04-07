"""
Player schema for serialization
"""
from marshmallow import fields, post_dump
from . import ma
from ..models.player import Player
from .device import DeviceSchema
from .clan import ClanSchema
from .campaign import CampaignSchema

class PlayerSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing Player objects"""
    class Meta:
        model = Player
        include_fk = True
    
    id = fields.Int(dump_only=True)
    player_id = fields.Str()
    credential = fields.Str()
    created = fields.DateTime(format="%Y-%m-%d %H:%M:%S%z")
    modified = fields.DateTime(format="%Y-%m-%d %H:%M:%S%z")
    last_session = fields.DateTime(format="%Y-%m-%d %H:%M:%S%z")
    total_spent = fields.Float()
    total_refund = fields.Float()
    total_transactions = fields.Int()
    last_purchase = fields.DateTime(format="%Y-%m-%d %H:%M:%S%z")
    level = fields.Int()
    xp = fields.Int()
    total_playtime = fields.Int()
    country = fields.Str()
    language = fields.Str()
    birthdate = fields.DateTime(format="%Y-%m-%d %H:%M:%S%z")
    gender = fields.Str()
    custom_field = fields.Str(attribute="_customfield")

    devices = fields.List(fields.Nested(DeviceSchema, only=("device_id", "model", "carrier", "firmware")))
    clan = fields.Nested(ClanSchema, only=("clan_id", "name"))
    campaigns = fields.List(fields.Nested(CampaignSchema, only=("campaign_id", "name")), attribute="campaigns")
    items = fields.Dict(keys=fields.Str(), values=fields.Int())
    
    @post_dump
    def process_items(self, data, **kwargs):
        """Process items to include quantities"""
        player = self.instance
        
        if player:
            data['items'] = player.get_items_dict()
        
        return data

# Initialize schemas
player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)
