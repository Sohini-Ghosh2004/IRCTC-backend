import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from app import create_app
from app.extensions import db
from app.models import Train

app = create_app()

train_names = [
    "Rajdhani Express",
    "Shatabdi Express",
    "Duronto Express",
    "Garib Rath",
    "Intercity Express",
    "Superfast Express"
]

with app.app_context():

    for i in range(50):   # create 50 trains

        train = Train(
            train_number=str(12000 + i),   # unique number
            train_name=random.choice(train_names),
            total_seats=random.choice([100, 120, 150])
        )

        db.session.add(train)

    db.session.commit()

print("Trains generated!")