from flask import Blueprint

common_bp = Blueprint("common" , __name__)

@common_bp.get("/health")
def health():
    return {"status": "ok",
            "module": "common",
            }