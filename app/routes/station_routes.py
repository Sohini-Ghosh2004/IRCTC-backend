from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.models.station import Station
from app.models.user import User
from app.extensions import db
from app.utils.decorators import admin_required

station_bp=Blueprint("stations",__name__)

@station_bp.route("/",methods=["POST"])
@jwt_required()
@admin_required
def add_station():
    data=request.get_json()
    station=Station(
        name=data["name"],
        code=data["code"]
    )
    db.session.add(station)
    db.session.commit()

    return jsonify({
        "success":True,
        "message":"Station added"
        }),201

@station_bp.route("/",methods=["GET"])
def get_stations():
    stations=Station.query.all()
    result=[]
    for s in stations:
        result.append({
            "id":s.station_id,
            "name":s.name,
            "code":s.code
        })
    return jsonify({
        "success":True,
        "data":result
    }),200    