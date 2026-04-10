from flask import Blueprint, jsonify
from utils import jwt_required

users_bp = Blueprint("users", __name__)


@users_bp.route("/users/me", methods=["GET"])
@jwt_required
def get_me(current_user):
    return jsonify(current_user.to_dict())
