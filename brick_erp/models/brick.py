from datetime import datetime
from ..extensions import db

class BrickItem(db.Model):
    __tablename__ = "brick_items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    rate_per_brick = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class Inventory(db.Model):
    __tablename__ = "inventory"
    id = db.Column(db.Integer, primary_key=True)
    brick_item_id = db.Column(db.Integer, db.ForeignKey("brick_items.id"), unique=True, nullable=False)
    quantity_on_hand = db.Column(db.Integer, nullable=False, default=0)
    last_updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    brick_item = db.relationship("BrickItem", backref=db.backref("inventory_record", uselist=False))
