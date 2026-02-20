import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # database setup
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    AUTO_CREATE_TABLES = True

    # JWT settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXP_SECONDS = int(os.getenv("JWT_EXP_SECONDS", "300"))  # 5 minutes default

    JWT_ISSUER = os.getenv("JWT_ISSUER", "flask-auth-skeleton")
    JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "flask-auth-client")