from flask import Blueprint, request, jsonify, render_template
from sqlalchemy.exc import IntegrityError
from email_validator import validate_email, EmailNotValidError

from app.extensions import db, bcrypt
from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# error helper for json
def error_response(code: str, message: str, *, field:str | None = None, status: int = 400):
    payload = {"ok": False, "error": {"code": code, "message": message}}
    if field:
        payload["error"]["field"] = field
    return jsonify(payload), status

# password validator
def validate_password(pw: str, min_length: int):
    if len(pw) < min_length:
        return False, f"Password must be at least {min_length} characters"
    return True, ""

@auth_bp.route("/ping", methods=['GET'])
def ping():
    return {
        "status": "ok",
        "module": "auth",
    }

@auth_bp.route('/register', methods=['GET'])
def register_page():
    return render_template("auth/register.html")

@auth_bp.route('/register', methods=['POST'])
def register():
    # 1 enforce json requests
    if not request.is_json:
        return error_response(
            "invalid content type",
            "Content-Type must be application/json",
            status=415
        )

    # 2 parse json safely
    data = request.get_json(silent=True) or {}
    raw_email = (data.get("email") or "").strip()
    password = (data.get("password") or "")

    # 3 validate password
    min_pw_length = 8
    if not password:
        return error_response(
            "validation error",
            "Password is required",
            field="password"
        )

    ok, msg = validate_password(password, min_pw_length)
    if not ok:
        return error_response(
            "validation error",
            f"Password must be at least {min_pw_length} characters",
            field="password"
        )

    # 4 rfc-aware email validation + normalization
    if not raw_email:
        return error_response(
            "validation error",
            "Email is required",
            field="email"
        )

    try:
        v = validate_email(raw_email, check_deliverability=False)
        email = v.normalized # normalized form
    except EmailNotValidError as e:
        return error_response(
            "validation error",
            str(e),
            field="email"
        )

    # 5 precheck for nicer error
    if User.query.filter_by(email=email).first() is not None:
        return error_response(
            "email taken",
            "An account with this email already exists",
            field="email",
            status=409
        )

    # password hashing
    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    # 7 create and commit to db
    user = User(email=email, password_hash=pw_hash)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error_response(
            "email taken",
            "An account with this email already exists",
            field="email",
            status=409
        )

    # 8 success response
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