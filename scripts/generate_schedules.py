import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from datetime import datetime, timedelta,timezone
from app import create_app
from app.extensions import db
from app.models import Train, TrainSchedule, TrainStop

app = create_app()

with app.app_context():
    trains = Train.query.all()
    count = 0

    for train in trains:
        stops = TrainStop.query.filter_by(train_id=train.train_id)\
                               .order_by(TrainStop.stop_order).all()
        if not stops:
            continue

        for i in range(5):  # next 5 days
            journey_date = (datetime.now(timezone.utc) + timedelta(days=i)).date()

            # skip if already exists (safe to re-run)
            existing = TrainSchedule.query.filter_by(
                train_id=train.train_id,
                journey_date=journey_date
            ).first()
            if existing:
                continue

            t_seats = train.total_seats 
            r_cap = max(1,int(t_seats * 0.20))    #20% of total seat=RAC

            schedule = TrainSchedule(
                train_id=train.train_id,
                journey_date=journey_date,
                total_seats=t_seats,          # Store the max capacity
                available_seats=t_seats,      # Start with a full, empty train
                rac_capacity=r_cap
            )
            db.session.add(schedule)
            count += 1

    db.session.commit()
    print(f"Done! {count} schedules created.")