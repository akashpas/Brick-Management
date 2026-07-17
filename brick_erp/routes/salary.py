from datetime import datetime
from decimal import Decimal
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required, current_user
from ..extensions import db
from ..models.employee import Employee
from ..models.salary import SalaryTransaction
from ..services.salary_service import compute_pending, pay_salary, SalaryPaymentError
from flask import current_app

salary_bp = Blueprint("salary", __name__, template_folder="../../templates/salary")

@salary_bp.get("/ledger")
@login_required
def ledger():
    employees = Employee.query.order_by(Employee.name.asc()).all()
    # Show latest 200 transactions
    tx = SalaryTransaction.query.order_by(SalaryTransaction.created_at.desc()).limit(200).all()
    pending_map = {e.id: compute_pending(e.id) for e in employees}
    return render_template("salary/ledger.html", employees=employees, tx=tx, pending_map=pending_map)

@salary_bp.post("/pay")
@login_required
def pay():
    try:
        employee_id = int(request.form["employee_id"])
        amount = Decimal(request.form["amount"])
        method = request.form.get("method", "CASH")
        remarks = request.form.get("remarks", "")
        allow_advances = current_app.config.get("SECURITY_ALLOW_ADVANCES", False)
        pay_salary(employee_id=employee_id, amount=amount, method=method, remarks=remarks,
                   created_by=current_user.id, allow_advances=allow_advances)
        flash("Salary payment recorded.", "success")
    except (KeyError, ValueError):
        flash("Invalid payment data.", "danger")
    except SalaryPaymentError as e:
        flash(str(e), "danger")
    return redirect(url_for("salary.ledger"))

@salary_bp.get("/export.csv")
@login_required
def export_csv():
    def generate():
        yield "id,employee_id,type,amount,method,txn_date,remarks\n"
        q = db.session.query(SalaryTransaction).order_by(SalaryTransaction.id.asc())
        for r in q:
            amt = f"{r.amount:.2f}"
            yield f"{r.id},{r.employee_id},{r.type},{amt},{r.payment_method or ''},{r.txn_date},{r.remarks or ''}\n"
    return Response(generate(), mimetype="text/csv",
                    headers={"Content-Disposition":"attachment; filename=salary_ledger.csv"})
