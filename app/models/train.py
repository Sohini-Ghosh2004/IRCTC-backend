from app.extensions import db

class Train(db.Model):
    __tablename__="trains"
    train_id=db.Column(db.Integer,primary_key=True)
    train_number=db.Column(db.String(20),unique=True,nullable=False)
    train_name=db.Column(db.String(100),nullable=False)
    total_seats=db.Column(db.Integer,nullable=False)
    
    stops=db.relationship("TrainStop",backref="train",lazy=True)
    schedules=db.relationship("TrainSchedule",backref="train",lazy=True)