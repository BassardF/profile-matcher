from flask_marshmallow import Marshmallow
from marshmallow import fields, post_dump
from models import Player, Device, Item, Clan, Campaign, PlayerItem

ma = Marshmallow()

class DeviceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Device
        include_fk = True
    
    id = fields.Int(dump_only=True)
    device_id = fields.Int()
    model = fields.Str()
    carrier = fields.Str()
    firmware = fields.Str()

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        include_fk = True
    
    id = fields.Int(dump_only=True)
    key = fields.Str()
    name = fields.Str()
    description = fields.Str()

class ClanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Clan
        include_fk = True
    
    clan_id = fields.Str()
    name = fields.Str()

class CampaignSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Campaign
        include_fk = True
    
    id = fields.Int(dump_only=True)
    campaign_id = fields.Str()
    name = fields.Str()

class PlayerSchema(ma.SQLAlchemyAutoSchema):
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
    active_campaigns = fields.List(fields.Nested(CampaignSchema, only=("campaign_id", "name")), attribute="campaigns")
    items = fields.Dict(keys=fields.Str(), values=fields.Int())
    
    @post_dump
    def process_items(self, data, **kwargs):
        player = self.instance
        
        if player:
            data['items'] = player.get_items_dict()
        
        return data

class MatcherSchema(ma.Schema):
    level = ma.Dict(keys=ma.Str(enum=['min', 'max']), values=ma.Int())
    has = ma.Dict(keys=ma.Str(enum=['country', 'items']), values=ma.List(ma.Str()))
    does_not_have = ma.Dict(keys=ma.Str(enum=['items']), values=ma.List(ma.Str()))

class APICampaignSchema(ma.Schema):
    id = ma.Str()
    game = ma.Str()
    name = ma.Str()
    priority = ma.Float()
    matchers = ma.Nested(MatcherSchema)
    start_date = ma.DateTime(format="%Y-%m-%d %H:%M:%S%z")
    end_date = ma.DateTime(format="%Y-%m-%d %H:%M:%S%z")
    enabled = ma.Boolean()
    last_updated = ma.DateTime(format="%Y-%m-%d %H:%M:%S%z")

# Initialize schemas
player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)
device_schema = DeviceSchema()
devices_schema = DeviceSchema(many=True)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
campaign_schema = CampaignSchema()
campaigns_schema = CampaignSchema(many=True)
api_campaign_schema = APICampaignSchema()
api_campaigns_schema = APICampaignSchema(many=True)