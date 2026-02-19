from flask import Flask

from .common.routes import common_bp
from .auth.routes import auth_bp

def create_app():
    app = Flask(__name__)

    # blueprint registers
    app.register_blueprint(common_bp)
    app.register_blueprint(auth_bp)

    return app