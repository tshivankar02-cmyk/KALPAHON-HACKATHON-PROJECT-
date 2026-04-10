import jwt 
import time
from functools import wraps
from flask import request, jsonify, current_app
from models import User


def create_token(user_id: int, email: str, role: str) -> str:
    payload = {
        "id": user_id,
        "email": email,
        "role": role,
        "iat": int(time.time()),
        "exp": int(time.time()) + 86400 * 7,
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")


def decode_token(token: str):
    return jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"message": "Missing or invalid token", "code": 401}), 401
        try:
            payload = decode_token(auth[7:])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired", "code": 401}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token", "code": 401}), 401
        user = User.query.get(payload.get("id"))
        if not user:
            return jsonify({"message": "User not found", "code": 401}), 401
        return f(user, *args, **kwargs)
    return decorated


def role_required(role: str):
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            if current_user.role != role:
                return jsonify({"message": f"Only {role} users can do this", "code": 403}), 403
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator
