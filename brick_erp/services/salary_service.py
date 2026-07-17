from decimal import Decimal
from datetime import date as date_cls
from ..extensions import db
from ..models.salary import SalaryTransaction
from ..models.employee import Employee

class SalaryPaymentError(Exception):
    pass

def compute_pending(employee_id:int):
    rows = SalaryTransaction.query.filter_by(employee_id=employee_id).all()
    total = Decimal("0.00")
    for r in rows:
        if r.type in ("EARNED", "BONUS"):
            total += Decimal(r.amount)
        elif r.type in ("PAID", "PENALTY"):
            total -= Decimal(r.amount)
        elif r.type == "ADJUSTMENT":
            total += Decimal(r.amount)
    return total.quantize(Decimal("0.01"))

def pay_salary(*, employee_id:int, amount, method:str, remarks:str, created_by:int, txn_date=None, allow_advances:bool=False):
    if txn_date is None:
        txn_date = date_cls.today()
    pending = compute_pending(employee_id)
    amount = Decimal(amount).quantize(Decimal("0.01"))
    if amount <= 0:
        raise SalaryPaymentError("Amount must be positive")

    if not allow_advances and amount > pending:
        raise SalaryPaymentError("Payment exceeds pending salary (advances not allowed)")

    # Ensure employee exists and is active
    emp = Employee.query.get(employee_id)
    if not emp or emp.status != "ACTIVE":
        raise SalaryPaymentError("Invalid or inactive employee")

    tx = SalaryTransaction(
        employee_id=employee_id,
        type="PAID",
        amount=amount,
        payment_method=method,
        remarks=remarks,
        created_by=created_by,
        txn_date=txn_date
    )
    db.session.add(tx)
    db.session.commit()
    return tx.id
