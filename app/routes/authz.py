from functools import wraps
from flask import request, jsonify, current_app, g

from jwt import ExpiredSignatureError, InvalidTokenError

from app.services.jwt_service import verify_access_token

def _auth_error(message: str, status:int = 400):
    return jsonify({"ok": False, "error": {"code": "Unauthorized", "message": message}}), status


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return  _auth_error("Missing or invalid Authorization header. Use: Bearer <token>", 401)

        token = header.removeprefix("Bearer ").strip()
        if not token:
            return _auth_error("Missing or invalid Authorization header. Use: Bearer <token>", 401)

        try:
            claims = verify_access_token(
                token,
                secret=current_app.config["JWT_SECRET_KEY"],
                algorithm=current_app.config["JWT_ALGORITHM"],
                issuer=current_app.config["JWT_ISSUER"],
                audience=current_app.config["JWT_AUDIENCE"],
            )
        except ExpiredSignatureError:
            return _auth_error("Token expired", 401)
        except InvalidTokenError:
            return _auth_error("Invalid token", 401)

        # store claims for route handlers / other decorators
        g.jwt_claims = claims
        return fn(*args, **kwargs)
    return wrapper

def require_role(required_role: str):
    def decorator(fn):
        @wraps(fn)
        @require_auth
        def wrapper(*args, **kwargs):
            claims = getattr(g, "jwt_claims", {}) or {}
            role = claims.get("role")

            if role != required_role:
                return jsonify({
                    "ok": False,
                    "error": {
                        "code": "Forbidden",
                        "message": f"Insufficient role. Required: {required_role}",
                    }
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
