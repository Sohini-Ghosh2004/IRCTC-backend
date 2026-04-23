from app.models import Train, Station
from sqlalchemy.orm import joinedload

def search_trains_service(source_id,dest_id,date_obj):
    
    source_station=Station.query.get(source_id)
    dest_station=Station.query.get(dest_id)

    if not source_station or not dest_station:
        return None,"Invalid Station"
    
    trains=Train.query.options(
        joinedload(Train.stops),
        joinedload(Train.schedules)
    ).all()
    result=[]
    for train in trains:
        stops=sorted(train.stops,key=lambda x: x.stop_order)
        src=None
        dest=None
        for stop in stops:
            if stop.station_id==source_id:
                src=stop
            if stop.station_id==dest_id:
                dest=stop
        if src and dest and src.stop_order < dest.stop_order: 
            for schedule in train.schedules:
                if schedule.journey_date == date_obj:
                    result.append({
                        "train":{
                            "train_id":train.train_id,
                            "train_name":train.train_name,
                            "train_number":train.train_number
                        },
                        "schedule_id": schedule.train_schedule_id,
                        "route":{
                            "from":source_station.name,
                            "to":dest_station.name                        
                        },
                        "timing":{
                            "departure":str(src.departure_time),
                            "arrival":str(dest.arrival_time),

                        },
                        
                        "available_seats":schedule.available_seats


                    })
    return result,None     


def search_stations_service(query):

    stations = Station.query.filter(
        Station.name.ilike(f"%{query}%")
    ).limit(10).all()

    result=[]
    for s in stations:
        result.append({
            "station_id":s.station_id,
            "name":s.name
        })
    return result,None