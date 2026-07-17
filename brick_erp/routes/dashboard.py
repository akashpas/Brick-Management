from flask import Blueprint, render_template
from flask_login import login_required
from ..extensions import db
from ..models.employee import Employee
from ..models.production import Production
from ..models.brick import Inventory, BrickItem
from ..models.salary import SalaryTransaction

dashboard_bp = Blueprint("dashboard", __name__, template_folder="../../templates/dashboard")

@dashboard_bp.get("/")
@login_required
def index():
    total_employees = db.session.query(Employee).count()
    workers = db.session.query(Employee).filter_by(type="WORKER").count()
    managers = db.session.query(Employee).filter_by(type="MANAGER").count()
    total_inventory = db.session.query(db.func.coalesce(db.func.sum(Inventory.quantity_on_hand), 0)).scalar()
    total_production = db.session.query(db.func.count(Production.id)).scalar()
    pending_salary_sum = 0
    # Simple aggregate: Earned - Paid + Adjustments/Bonus - Penalty
    totals = db.session.query(
        SalaryTransaction.type,
        db.func.coalesce(db.func.sum(SalaryTransaction.amount), 0)
    ).group_by(SalaryTransaction.type).all()
    sums = {t: float(a) for t, a in totals}
    pending_salary_sum = (sums.get("EARNED", 0) + sums.get("BONUS", 0) + sums.get("ADJUSTMENT", 0)
                          - sums.get("PAID", 0) - sums.get("PENALTY", 0))
    brick_items = db.session.query(BrickItem).all()
    return render_template(
        "dashboard/index.html",
        total_employees=total_employees,
        workers=workers,
        managers=managers,
        total_inventory=total_inventory,
        total_production=total_production,
        pending_salary_sum=pending_salary_sum,
        brick_items=brick_items
    )
