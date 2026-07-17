# Brick Plant ERP Management System (MVP)

A Flask-based ERP MVP for a brick manufacturing plant:
- Admin and Site Manager roles
- Employee management (workers/managers)
- Brick types and inventory
- Production entry with automatic inventory increment and salary-earned accrual
- Salary ledger (Earned/Paid/Adjustments)
- Simple dashboard and CSV exports

Tech stack: Flask, SQLAlchemy, Flask-Migrate, Flask-Login, Bootstrap (templates).

## Quick start (development)
1) Python 3.11+
2) Create virtualenv and install:
   - python -m venv .venv
   - source .venv/bin/activate  (Windows: .venv\\Scripts\\activate)
   - pip install -r requirements.txt
3) Set environment (optional):
   - cp .env.example .env  (edit as needed)
   - export FLASK_APP=app.py
   - export FLASK_ENV=development
4) Initialize DB (SQLite by default):
   - flask db init
   - flask db migrate -m "init"
   - flask db upgrade
5) Create an admin user:
   - flask create-admin --username admin --password admin123
6) Run:
   - flask run
   - Open http://127.0.0.1:5000

For PostgreSQL:
- Set DATABASE_URL, e.g.:
  export DATABASE_URL="postgresql+psycopg2://user:pass@localhost:5432/brick_erp"

## Notes
- Default login view at /auth/login
- Admin-only actions include salary payments and config
- Code is modular to extend per SRS
