from app.extensions import db

class Booking(db.Model):
    __tablename__="bookings"

    booking_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.user_id"),nullable=False)
    train_schedule_id=db.Column(db.Integer,db.ForeignKey("train_schedules.train_schedule_id"),nullable=False)
    seat_number=db.Column(db.String(10),nullable=True)
    rac_number = db.Column(db.Integer, nullable=True)
    waitlist_number=db.Column(db.Integer,nullable=True)
    status=db.Column(db.String(20),default="CONFIRMED")
    created_at=db.Column(db.DateTime,server_default=db.func.now())
    