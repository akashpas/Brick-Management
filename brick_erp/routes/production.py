from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required, current_user
from ..extensions import db
from ..models.employee import Employee
from ..models.brick import BrickItem, Inventory
from ..models.production import Production
from ..services.production_service import create_production, ProductionError

production_bp = Blueprint("production", __name__, template_folder="../../templates/production")

@production_bp.get("/")
@login_required
def list_production():
    rows = Production.query.order_by(Production.prod_date.desc(), Production.id.desc()).limit(100).all()
    items = BrickItem.query.filter_by(active=True).all()
    workers = Employee.query.filter_by(type="WORKER", status="ACTIVE").all()
    return render_template("production/list.html", rows=rows, items=items, workers=workers)

@production_bp.post("/")
@login_required
def add_production():
    try:
        brick_item_id = int(request.form["brick_item_id"])
        quantity = int(request.form["quantity"])
        employee_id = int(request.form["employee_id"])
        prod_date = datetime.strptime(request.form.get("prod_date"), "%Y-%m-%d").date() if request.form.get("prod_date") else None
        pid = create_production(
            brick_item_id=brick_item_id,
            quantity=quantity,
            employee_id=employee_id,
            created_by=current_user.id,
            prod_date=prod_date
        )
        flash(f"Production recorded (ID {pid}). Inventory and earned salary updated.", "success")
    except (KeyError, ValueError):
        flash("Invalid form data.", "danger")
    except ProductionError as e:
        flash(str(e), "danger")
    return redirect(url_for("production.list_production"))

@production_bp.get("/export.csv")
@login_required
def export_csv():
    def generate():
        yield "id,prod_date,brick_item,quantity,employee_id\n"
        q = db.session.query(Production).order_by(Production.id.asc())
        for r in q:
            name = r.brick_item.name if r.brick_item else ""
            yield f"{r.id},{r.prod_date},{name},{r.quantity},{r.employee_id}\n"
    return Response(generate(), mimetype="text/csv",
                    headers={"Content-Disposition":"attachment; filename=production.csv"})
