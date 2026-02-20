from flask import Flask

# import modules
import os


# import applications
from app.extensions import db
from app.config import Config, instance_path
from app.models.user import User

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # application db setup
    os.makedirs(instance_path, exist_ok=True) # ensure db directory exists
    db.init_app(app)

    # blueprint registers
    # import routes
    from .common.routes import common_bp
    from .auth.routes import auth_bp

    app.register_blueprint(common_bp)
    app.register_blueprint(auth_bp)

    # create tables once
    with app.app_context():
        from app import models
        db.create_all()


    return app