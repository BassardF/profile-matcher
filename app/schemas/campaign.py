"""
Campaign schema for serialization
"""
from marshmallow import fields
from . import ma
from ..models.campaign import Campaign

class CampaignSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing Campaign objects"""
    class Meta:
        model = Campaign
        include_fk = True
    
    id = fields.Int(dump_only=True)
    campaign_id = fields.Str()
    name = fields.Str()

# Initialize schemas
campaign_schema = CampaignSchema()
campaigns_schema = CampaignSchema(many=True)
