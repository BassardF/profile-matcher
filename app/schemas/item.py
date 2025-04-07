"""
Item schema for serialization
"""
from marshmallow import fields
from . import ma
from ..models.item import Item

class ItemSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing Item objects"""
    class Meta:
        model = Item
        include_fk = True
    
    id = fields.Int(dump_only=True)
    key = fields.Str()
    name = fields.Str()
    description = fields.Str()

# Initialize schemas
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
