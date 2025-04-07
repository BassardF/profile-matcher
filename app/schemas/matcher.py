"""
Matcher and API Campaign schemas for serialization
"""
from marshmallow import fields
from . import ma

class MatcherSchema(ma.Schema):
    """Schema for campaign matcher criteria"""
    level = ma.Dict(keys=ma.Str(enum=['min', 'max']), values=ma.Int())
    has = ma.Dict(keys=ma.Str(enum=['country', 'items']), values=ma.List(ma.Str()))
    does_not_have = ma.Dict(keys=ma.Str(enum=['items']), values=ma.List(ma.Str()))

class APICampaignSchema(ma.Schema):
    """Schema for external API campaign format"""
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
api_campaign_schema = APICampaignSchema()
api_campaigns_schema = APICampaignSchema(many=True)
