from functools import wraps
from flask import request, jsonify

from src.infra.config.config import get_settings
from src.interface.web.middleware.jwt_handler import JWTHandler

settings = get_settings()

def auth_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token is None:
            return jsonify({"detail": "UNAUTHORIZED"}), 401
        token = token.removeprefix("Bearer ").strip()
        payload = JWTHandler.verify_access_token(token)
        if payload is None:
            return jsonify({"detail": "UNAUTHORIZED"}), 401

        return func(*args, **kwargs)

    return decorator

def state_auth_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token is None:
            return jsonify({"detail": "UNAUTHORIZED"}), 401
        token = token.removeprefix("Bearer ").strip()
        payload = JWTHandler.verify_access_token(token)
        if payload is None:
            return jsonify({"detail": "UNAUTHORIZED"}), 401

        state = {
            "sub": payload["sub"],
            "id": payload["id"]
        }
        return func(state, *args, **kwargs)

    return decorator
