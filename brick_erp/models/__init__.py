# Import models so Flask-Migrate (Alembic) can detect them
from .user import User  # noqa: F401
from .employee import Employee  # noqa: F401
from .brick import BrickItem, Inventory  # noqa: F401
from .production import Production  # noqa: F401
from .salary import SalaryTransaction  # noqa: F401

def all_models():
    # Placeholder to make imports explicit for linters
    return [User, Employee, BrickItem, Inventory, Production, SalaryTransaction]
