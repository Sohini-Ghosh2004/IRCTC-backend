import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from sqlalchemy.exc import IntegrityError

import json
from app import create_app
from app.extensions import db
from app.models import Station

app=create_app()
with app.app_context():
    with open("data/railwayStationsList.json",encoding="utf-8") as file:
        data=json.load(file)

        for row in data["stations"]:
            station=Station(
                code=row.get("stnCode"),
                name=row.get("stnName"),
                city=row.get("stnCity",""),
                
            )
            db.session.add(station)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                continue
    print("Stations imported!")        