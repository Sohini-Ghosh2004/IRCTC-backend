"""
Verifies station pairs and stop orders for active trains.
Used to ensure data integrity before testing booking logic.
"""
from app import create_app
from app.models import TrainStop
app = create_app()
with app.app_context():
    stops = TrainStop.query.filter_by(train_id=1).order_by(TrainStop.stop_order).all()
    for s in stops:
        print(s.stop_order, s.station_id)

