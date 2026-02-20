import os
from pathlib import Path

# project root = folder that contains run.py
base_directory = Path(__file__).resolve().parents[1]
instance_path = base_directory / "instance"
db_path = instance_path / "dev.db"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + db_path.as_posix(),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

