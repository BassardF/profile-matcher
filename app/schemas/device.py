"""
Device schema for serialization
"""
from marshmallow import fields
from . import ma
from ..models.device import Device

class DeviceSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing Device objects"""
    class Meta:
        model = Device
        include_fk = True
    
    id = fields.Int(dump_only=True)
    device_id = fields.Int()
    model = fields.Str()
    carrier = fields.Str()
    firmware = fields.Str()

# Initialize schemas
device_schema = DeviceSchema()
devices_schema = DeviceSchema(many=True)
