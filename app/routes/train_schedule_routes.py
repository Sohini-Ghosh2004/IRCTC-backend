from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required
from app.models.train_schedule import TrainSchedule
from app.models.train import Train
from app.extensions import db
from app.utils.decorators import admin_required
from datetime import datetime

train_schedule_bp=Blueprint("train_schedules",__name__)

@train_schedule_bp.route("/",methods=["POST"])
@jwt_required()
@admin_required
def add_train_schedule():
    data=request.get_json()

    journey_date=datetime.strptime(data["journey_date"], "%Y-%m-%d").date()
    train=Train.query.get(data["train_id"])

    schedule=TrainSchedule(
        train_id=data["train_id"],
        journey_date=journey_date,
        available_seats=train.total_seats
    )
    db.session.add(schedule)
    db.session.commit()
    return jsonify({
        "success":True,
        "message":"Schedule added",
        "data":{
            "schedule_id": schedule.train_schedule_id
        }
    }),201

@train_schedule_bp.route("/",methods=["GET"])
def get_schedules():
    train_id=request.args.get("train_id")
    journey_date=request.args.get("journey_date")
    query=TrainSchedule.query
    if train_id:
        query=query.filter_by(train_id=train_id)
    if journey_date:
        date_obj=datetime.strptime(journey_date,"%Y-%m-%d").date()
        query=query.filter_by(journey_date=date_obj)  
    train_schedules=query.all()
          
    result=[]
    for s in train_schedules:
        result.append({
            "train_schedule_id":s.train_schedule_id,
            "train_id":s.train_id,
            "journey_date":str(s.journey_date),
            "available_seats":s.available_seats
        })
    return jsonify({
        "success":True,
        "data":result
    }),200