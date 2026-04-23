from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required
from app.models.train_stop import TrainStop
from app.extensions import db
from app.utils.decorators import admin_required
from datetime import datetime

train_stop_bp=Blueprint("train_stops",__name__)

@train_stop_bp.route("/",methods=["POST"])
@jwt_required()
@admin_required
def add_train_stop():
    data=request.get_json()
    arrival_time=datetime.strptime(data["arrival_time"],"%H:%M:%S").time()
    departure_time=datetime.strptime(data["departure_time"],"%H:%M:%S").time()
    
    existing_stop_order=TrainStop.query.filter_by(
        train_id=data["train_id"],
        stop_order=data["stop_order"]
    ).first()
    if existing_stop_order:
        return jsonify({
            "success":False,
            "message":"stop_order already exists"
        }),400
    
    existing_station=TrainStop.query.filter_by(
        train_id=data["train_id"],
        station_id=data["station_id"]
    ).first()
    if existing_station:
        return jsonify({
            "success":False,
            "message":"station already added"
        }),400
    
    
    
    stop=TrainStop(
        train_id=data["train_id"],
        station_id=data["station_id"],
        stop_order=data["stop_order"],
        arrival_time=arrival_time,
        departure_time=departure_time
    )
    db.session.add(stop)
    db.session.commit()
    return jsonify({
        "success":True,
        "message":"Train stop added"
    }),201

@train_stop_bp.route("/<int:train_id>",methods=["GET"])
def get_train_stops(train_id):
    stops=TrainStop.query.filter_by(train_id=train_id).all()
    result=[]
    for s in sorted(stops,key=lambda x:x.stop_order):
        result.append({
            "station_id":s.station_id,
            "station_name":s.station.name,         #relationship used
            "stop_order":s.stop_order,
            "arrival_time":str(s.arrival_time),
            "departure_time":str(s.departure_time)
        })
    return jsonify({
        "success":True,
        "data":result
    }),200