from flask import request,jsonify,Blueprint
from app.extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity


auth_bp=Blueprint("auth",__name__)


@auth_bp.route("/register",methods=["POST"])
def register():
    data=request.get_json()
    hashed_password=generate_password_hash(data["password"])
    user=User(
        username=data["username"],
        email=data["email"],
        password_hash=hashed_password
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "success":True,
        "message":"User registered successfully"
    }),201

@auth_bp.route("/login",methods=["POST"])
def login():
    data=request.get_json()
    user=User.query.filter_by(email=data["email"]).first()

    if not user:
        return jsonify({
            "success":False,
            "message":"User not found"
        }),404
    
    if not check_password_hash(user.password_hash,data["password"]):
        return jsonify({
            "success":False,
            "message":"Invalid credentials"
        }),401
    
    access_token=create_access_token(identity=str(user.user_id))

    return jsonify({
        "success":True,
        "message":"Login Successful",
        "access_token":access_token
    }),200

@auth_bp.route("/me",methods=["GET"])
@jwt_required()
def get_me():
    user_id=get_jwt_identity()
    user=User.query.get(user_id)

    return jsonify({
        "success":True,
        "data":{
            "user_id":user.user_id,
            "username":user.username,
            "email":user.email            
        }
    }),200