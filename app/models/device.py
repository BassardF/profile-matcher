"""
Device model
"""
from . import db

class Device(db.Model):
    """Device model representing player devices"""
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, nullable=False)
    model = db.Column(db.String)
    carrier = db.Column(db.String)
    firmware = db.Column(db.String)
    
    __table_args__ = (
        db.UniqueConstraint('device_id', 'model', name='uix_device_id_model'),
    )
