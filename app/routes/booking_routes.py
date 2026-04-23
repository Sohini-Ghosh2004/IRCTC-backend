from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.models.train_schedule import TrainSchedule
from app.models.booking import Booking
from app.extensions import db
from app.services.booking_service import book_ticket_service,cancel_booking_service,get_bookings_service
from app.schemas.booking_schema import BookingCreateSchema,BookingSchema
from marshmallow import ValidationError

booking_bp=Blueprint("bookings",__name__)


@booking_bp.route("/",methods=["POST"])
@jwt_required()
def book_ticket():
    data=request.get_json(silent=True)
    user_id=get_jwt_identity()

    if not data:
        return jsonify({
            "success":False,
            "message": "Request body must be JSON"
        }), 400
    
    schema=BookingCreateSchema()
    try:
        validated_data=schema.load(data)
    except ValidationError as err:
        return jsonify({
            "success":False,
            "errors":err.messages
        }),400 
    
    schedule_id=validated_data["train_schedule_id"]   

    booking, error=book_ticket_service(user_id,schedule_id)
    if error:
        return jsonify({
            "success":False,
            "message":error
        }),400
    
    response_schema=BookingSchema()

    return jsonify({
        "success":True,
        "message": f"Added as {booking.status}",
        "data": response_schema.dump(booking)
    }), 201

@booking_bp.route("/my",methods=["GET"])
@jwt_required()
def get_bookings():
    user_id=get_jwt_identity()
    result,error=get_bookings_service(user_id)
    if error:
        return jsonify({"message":error}),400
    return jsonify({ 
        "success":True,
        "data":result
        }),200
    
@booking_bp.route("/<int:booking_id>",methods=["DELETE"])
@jwt_required()
def cancel_booking(booking_id):
    user_id=get_jwt_identity()
    booking, error= cancel_booking_service(user_id,booking_id)
    if error:
        return jsonify({
            "success":False,
            "message":error
        }),400
    return jsonify({
        "success":True,
        "message":"Booking Cancelled"
    }),200