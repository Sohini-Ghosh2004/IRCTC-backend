from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required
from app.models.train import Train
from app.extensions import db
from app.utils.decorators import admin_required

train_bp=Blueprint("trains",__name__)

@train_bp.route("/",methods=["POST"])
@jwt_required()
@admin_required
def add_train():
    data=request.get_json()
    train=Train(
        train_number=data["train_number"],
        train_name=data["train_name"],
        total_seats=data["total_seats"]
    )
    db.session.add(train)
    db.session.commit()
    return jsonify({
        "success":True,
        "message":"Train added"
    }),201

@train_bp.route("/",methods=["GET"])
def get_trains():
    trains=Train.query.all()
    result=[]
    for t in trains:
        result.append({
            "id": t.train_id,
            "name": t.train_name,
            "number":t.train_number,
            "total_seats":t.total_seats
        })
    return jsonify({
        "success":True,
        "data":result
    }),200