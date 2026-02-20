import uuid
from datetime import datetime, timezone
from app.extensions import db

class User(db.Model):
    __tablename__ = "users"

    # internal ID (primary key)
    id = db.Column(db.Integer, primary_key=True)

    # public UUID
    uuid = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )

    # core fields
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
