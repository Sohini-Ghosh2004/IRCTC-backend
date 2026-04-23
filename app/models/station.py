from app.extensions import db

class Station(db.Model):
    __tablename__="stations"

    station_id=db.Column(db.Integer,primary_key=True)
    code=db.Column(db.String(10),nullable=False,unique=True)
    name=db.Column(db.String(100),nullable=False)
    city=db.Column(db.String(100))
    state=db.Column(db.String(100))
    stops=db.relationship("TrainStop",backref="station",lazy=True)