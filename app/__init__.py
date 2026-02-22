import os
from flask import Flask

# import applications
from app.extensions import db
from app.config import Config

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # ensure instance/ exists
    os.makedirs(app.instance_path, exist_ok=True) # ensure db directory exists
    # initialize db
    db.init_app(app)

    # blueprint registers
    from app.routes import auth_bp, common_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(common_bp)

    # Create tables in development only (optional)
    if app.config.get("AUTO_CREATE_TABLES", True):
        with app.app_context():
            from app import models  # registers models
            db.create_all()


    return app
