from app.extensions import db

class TrainSchedule(db.Model):
    __tablename__="train_schedules"
    
    train_schedule_id=db.Column(db.Integer,primary_key=True)
    train_id=db.Column(db.Integer,db.ForeignKey("trains.train_id"),nullable=False)
    journey_date=db.Column(db.Date,nullable=False)
    available_seats=db.Column(db.Integer,nullable=False)
    total_seats=db.Column(db.Integer,nullable=False)
    rac_capacity=db.Column(db.Integer,nullable=False)
    created_at=db.Column(db.DateTime,server_default=db.func.now())
    __table_args__ = (
        db.UniqueConstraint("train_id", "journey_date"),
    )