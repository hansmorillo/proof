from flask import Blueprint, request, jsonify, render_template

from app.services.auth_service import register_user, ServiceError, login_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def error_response(code: str, message: str, *, field: str | None = None, status: int = 400):
    payload = {"ok": False, "error": {"code": code, "message": message}}
    if field:
        payload["error"]["field"] = field
    return jsonify(payload), status

@auth_bp.get('/ping')
def ping():
    return {"status": "ok", "module": "auth"}

@auth_bp.get("/register")
def register_page():
    return render_template("auth/register.html")

@auth_bp.post('/register')
def register():
    # enforce json
    if not request.is_json:
        return error_response("Invalid Content Type", "Content-Type must be application/json", status=415)

    data = request.get_json(silent=True) or {}
    raw_email = (data.get("email") or "")
    password = (data.get("password") or "")

    try:
        user = register_user(raw_email, password)
    except ServiceError as e:
        return error_response(e.code, e.message, field=e.field, status=e.status)

    return jsonify({
        "ok": True,
        "data": {
            "id": user.id,
            "uuid": user.uuid,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat(),
        }
    }), 201


@auth_bp.get("/login")
def login_page():
    return render_template("auth/login.html")

@auth_bp.post('/login')
def login():
    if not request.is_json:
        return error_response("Invalid Content Type", "Content-Type must be application/json", status=415)

    data = request.get_json(silent=True) or {}

    try:
        result = login_user(
            email_raw=data.get("email"),
            password=data.get("password"),
        )
        return jsonify({"ok": True, "data": result}), 200

    except ServiceError as e:
        return error_response(e.code, e.message, field=e.field, status=e.status)
