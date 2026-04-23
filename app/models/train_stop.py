from app.extensions import db

class TrainStop(db.Model):
    __tablename__="train_stops"
    stop_id=db.Column(db.Integer,primary_key=True)
    train_id=db.Column(db.Integer,db.ForeignKey("trains.train_id"),nullable=False)
    station_id=db.Column(db.Integer,db.ForeignKey("stations.station_id"),nullable=False)
    stop_order=db.Column(db.Integer,nullable=False)
    arrival_time=db.Column(db.Time)
    departure_time=db.Column(db.Time)

    