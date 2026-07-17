from datetime import datetime
from ..extensions import db

class Employee(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    contact = db.Column(db.String(50))
    type = db.Column(db.String(20), nullable=False, default="WORKER")  # WORKER | MANAGER
    status = db.Column(db.String(20), nullable=False, default="ACTIVE")  # ACTIVE | INACTIVE
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
