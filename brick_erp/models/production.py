from datetime import datetime, date
from ..extensions import db

class Production(db.Model):
    __tablename__ = "production"
    id = db.Column(db.Integer, primary_key=True)
    prod_date = db.Column(db.Date, default=date.today, nullable=False)
    brick_item_id = db.Column(db.Integer, db.ForeignKey("brick_items.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)  # worker
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    edit_reason = db.Column(db.String(255))

    brick_item = db.relationship("BrickItem")
