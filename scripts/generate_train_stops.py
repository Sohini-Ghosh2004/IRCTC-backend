import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import random 
from datetime import time,timedelta,datetime
from app import create_app
from app.extensions import db
from app.models import Train,Station,TrainStop

app=create_app()
with app.app_context():
    trains=Train.query.all()
    stations =Station.query.limit(100).all()   #frist 100 station for simplicity
    
    for train in trains:
        num_stops=random.randint(5,10) #random route length
        route_stations=random.sample(stations,num_stops) #random station(no repeat)
        current_time=datetime.strptime("06:00","%H:%M")
        
        for i, station in enumerate(route_stations):

            arrival = current_time.time()
            departure = (current_time + timedelta(minutes=10)).time()

            stop = TrainStop(
                train_id=train.train_id,
                station_id=station.station_id,
                stop_order=i + 1,
                arrival_time=arrival,
                departure_time=departure
            )

            db.session.add(stop)

            # next station after some travel time
            current_time += timedelta(minutes=random.randint(60, 180))

    db.session.commit()

print("Train routes generated!")