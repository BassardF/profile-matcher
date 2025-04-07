"""
Clan schema for serialization
"""
from marshmallow import fields
from . import ma
from ..models.clan import Clan

class ClanSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing Clan objects"""
    class Meta:
        model = Clan
        include_fk = True
    
    clan_id = fields.Str()
    name = fields.Str()
