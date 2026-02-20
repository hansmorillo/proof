from flask import Blueprint, render_template

common_bp = Blueprint("common" , __name__)

@common_bp.get("/health")
def health():
    return {"status": "ok",
            "module": "common",
            }

@common_bp.get("/")
def index():
    return render_template("home.html")
