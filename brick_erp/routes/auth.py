from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from ..extensions import db, login_manager
from ..models.user import User

auth_bp = Blueprint("auth", __name__, template_folder="../../templates/auth")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    return render_template("auth/login.html")

@auth_bp.post("/login")
def login_post():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password) or user.status != "APPROVED":
        flash("Invalid credentials or account not approved", "danger")
        return redirect(url_for("auth.login"))
    login_user(user, remember=True)
    return redirect(url_for("dashboard.index"))

@auth_bp.post("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("auth.login"))
