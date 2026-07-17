import os
from flask import Flask
from .extensions import db, migrate, login_manager, csrf
from .routes.auth import auth_bp
from .routes.dashboard import dashboard_bp
from .routes.production import production_bp
from .routes.salary import salary_bp
from .models.user import User
from .models import all_models  # noqa: F401 (ensures models are imported for migrations)
from config import get_config

def create_app():
    app = Flask(__name__, instance_relative_config=True, template_folder="../templates")
    app.config.from_object(get_config())

    os.makedirs(app.instance_path, exist_ok=True)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Auth setup
    login_manager.login_view = "auth.login"

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(production_bp, url_prefix="/production")
    app.register_blueprint(salary_bp, url_prefix="/salary")

    # CLI to create admin
    @app.cli.command("create-admin")
    def create_admin():
        """Create an admin user: flask create-admin --username admin --password secret"""
        import click
        @click.option("--username", prompt=True)
        @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
        def inner(username, password):
            from .models.user import User
            from werkzeug.security import generate_password_hash
            if User.query.filter_by(username=username).first():
                click.echo("User already exists.")
                return
            u = User(username=username, role="ADMIN", status="APPROVED",
                     password_hash=generate_password_hash(password))
            db.session.add(u)
            db.session.commit()
            click.echo("Admin created.")
        return inner()

    @app.route("/")
    def root():
        from flask import redirect, url_for
        return redirect(url_for("dashboard.index"))

    return app
