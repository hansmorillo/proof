from dataclasses import dataclass
from typing import Optional

from sqlalchemy.exc import IntegrityError
from email_validator import validate_email, EmailNotValidError

import app.config as config
from app import Config

from app.extensions import db, bcrypt
from app.models import User
from app.services.jwt_service import issue_access_token


@dataclass
class ServiceError(Exception):
    code: str
    message: str
    field: Optional[str] = None
    status: int = 400


def _validate_password(pw: str, min_length: int = 8) -> None:
    if not pw:
        raise ServiceError(
            "Validation Error",
            "Password is required",
            field="password",
            status=400
        )
    if len(pw) < min_length:
        raise ServiceError(
            "Validation Error",
            f"Password must be at least {min_length} characters long",
            field="password",
            status=400,
        )


def _normalize_email(raw_email: str) -> str:
    if not raw_email:
        raise ServiceError(
            "Validation Error",
            "Email is required",
            field="email",
            status=400,
        )
    try:
        v = validate_email(raw_email, check_deliverability=False)   # can change to true if need email MFA
        return v.normalized
    except EmailNotValidError as e:
        raise ServiceError(
            "Validation Error",
            str(e),
            field="email",
            status=400,
        )


def register_user(email_raw: str, password: str) -> User:
    """
    Logic Below
    1. validate inputs
    2. normalize email
    3. enforce unique email
    4. hash password
    5. create new user
    """
    email = _normalize_email(email_raw or "").strip()
    _validate_password(password, min_length=8)

    # pre-check for nicer error
    if User.query.filter_by(email=email).first() is not None:
        raise ServiceError(
            "Email already registered!",
            "An account with this email already exists",
            field="email",
            status=400,
        )

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(email=email, password_hash=password_hash)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ServiceError(
            "Database Error",
            str(e),
            status=400,
        )

    return user


def login_user(email_raw: str, password: str) -> dict:
    """
    Logic:
    1. validate inputs
    2. normalize email
    3. fetch user
    4. verify password hash
    5. issue JWT access token
    """

    email = _normalize_email(email_raw or "").strip()
    _validate_password(password, min_length=8)

    user = User.query.filter_by(email=email).first()
    if user is None:
        # generic to prevent account enumeration
        raise ServiceError(
            "Authentication Error",
            "Invalid Credentials",
            status=401,
        )

    if not bcrypt.check_password_hash(user.password_hash, password):
        raise ServiceError(
            "Authentication Error",
            "Invalid Credentials",
            status=401,
        )

    token = issue_access_token(
        sub=str(user.id),
        role=getattr(user, "role", "user"),      # role claim (default if don't have column yet)
        secret=str(Config.JWT_SECRET_KEY),
        algorithm=str(Config.JWT_ALGORITHM),
        issuer=str(Config.JWT_ISSUER),
        audience=str(Config.JWT_AUDIENCE),
        exp_seconds=int(Config.JWT_EXP_SECONDS),
    )

    return {
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": int(Config.JWT_EXP_SECONDS),
    }
