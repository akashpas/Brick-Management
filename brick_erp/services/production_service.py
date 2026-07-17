from decimal import Decimal
from sqlalchemy.exc import IntegrityError
from ..extensions import db
from ..models.brick import Inventory
from ..models.production import Production
from ..models.salary import SalaryTransaction
from ..models.brick import BrickItem

class ProductionError(Exception):
    pass

def create_production(*, brick_item_id:int, quantity:int, employee_id:int, created_by:int, prod_date):
    if quantity <= 0:
        raise ProductionError("Quantity must be greater than zero")

    # Resolve rate
    brick_item = BrickItem.query.get(brick_item_id)
    if not brick_item or not brick_item.active:
        raise ProductionError("Invalid or inactive brick type")
    rate = Decimal(brick_item.rate_per_brick or 0)

    try:
        prod = Production(
            brick_item_id=brick_item_id,
            quantity=quantity,
            employee_id=employee_id,
            created_by=created_by,
            prod_date=prod_date
        )
        db.session.add(prod)

        inv = Inventory.query.filter_by(brick_item_id=brick_item_id).first()
        if not inv:
            inv = Inventory(brick_item_id=brick_item_id, quantity_on_hand=0)
            db.session.add(inv)
        inv.quantity_on_hand = int(inv.quantity_on_hand) + int(quantity)

        earned_amount = (Decimal(quantity) * rate).quantize(Decimal("0.01"))
        ledger = SalaryTransaction(
            employee_id=employee_id,
            type="EARNED",
            amount=earned_amount,
            payment_method=None,
            remarks=f"Earned from production ID pending",
            created_by=created_by,
            reference_type="PRODUCTION"
        )
        db.session.add(ledger)

        db.session.commit()
        # Update remarks with actual production id if needed
        ledger.remarks = f"Earned from production ID {prod.id}"
        db.session.commit()
        return prod.id
    except IntegrityError as e:
        db.session.rollback()
        raise ProductionError("Database error while creating production") from e
