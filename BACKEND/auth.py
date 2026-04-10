import re
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from utils import create_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    d = request.get_json(silent=True) or {}
    name = (d.get("name") or "").strip()
    email = (d.get("email") or "").strip().lower()
    password = d.get("password") or ""
    role = d.get("role") or ""
    bio = (d.get("bio") or "").strip() or None

    if not name or not email or not password or not role:
        return jsonify({"message": "name, email, password, and role are required", "code": 400}), 400
    if role not in ("INFLUENCER", "BRAND"):
        return jsonify({"message": "role must be INFLUENCER or BRAND", "code": 400}), 400
    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters", "code": 400}), 400
    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        return jsonify({"message": "Invalid email format", "code": 400}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered", "code": 409}), 409

    user = User(name=name, email=email, password_hash=generate_password_hash(password), role=role, bio=bio)
    db.session.add(user)
    db.session.commit()
    token = create_token(user.id, user.email, user.role)
    return jsonify({"token": token, "user": user.to_dict()}), 201


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    d = request.get_json(silent=True) or {}
    email = (d.get("email") or "").strip().lower()
    password = d.get("password") or ""
    if not email or not password:
        return jsonify({"message": "email and password are required", "code": 400}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid email or password", "code": 401}), 401
    token = create_token(user.id, user.email, user.role)
    return jsonify({"token": token, "user": user.to_dict()})
