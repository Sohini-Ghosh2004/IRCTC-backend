from flask import request,jsonify,Blueprint
from app.extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from app.utils.decorators import admin_required
admin_bp=Blueprint("admin",__name__)

@admin_bp.route("/dashboard",methods=["GET"])
@jwt_required()
@admin_required
def admin_dashboard():
    return jsonify({
        "success":True,
        "message":"Welcome Admin"
    }),200
