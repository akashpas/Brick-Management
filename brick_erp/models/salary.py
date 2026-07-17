from datetime import datetime, date
from ..extensions import db

class SalaryTransaction(db.Model):
    __tablename__ = "salary_transactions"
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # EARNED | PAID | ADJUSTMENT | BONUS | PENALTY
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    payment_method = db.Column(db.String(20))  # CASH | BANK_TRANSFER | UPI | CHEQUE (for PAID)
    remarks = db.Column(db.String(255))
    txn_date = db.Column(db.Date, default=date.today, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    reference_type = db.Column(db.String(30))  # e.g., PRODUCTION
    reference_id = db.Column(db.Integer)       # id of production row etc.
    reversed_by = db.Column(db.Integer)        # optional link for reversals
