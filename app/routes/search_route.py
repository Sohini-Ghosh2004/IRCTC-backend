from flask import Blueprint,request,jsonify
from app.models import TrainStop,TrainSchedule,Train,Station
from datetime import datetime
from sqlalchemy.orm import aliased
from app.extensions import db
from sqlalchemy.orm import joinedload
from app.services.search_service import search_trains_service,search_stations_service
from app.schemas.station_schema import TrainResultSchema  

search_bp=Blueprint("search",__name__)

#search trains
@search_bp.route("/",methods=['GET'])
def search_trains():
    source_id=request.args.get("source_id")
    dest_id=request.args.get("dest_id")
    journey_date=request.args.get("date")

    if not source_id or not dest_id or not journey_date:
        return jsonify({
            "success":False,
            "message":"Missing parameters"
        }),400
    try:
        source_id=int(source_id)
        dest_id=int(dest_id)
        date_obj=datetime.strptime(journey_date,"%Y-%m-%d").date()
    except:
        return jsonify({
            "success":False,
            "message":"Invalid input format"
        }),400
    result,error=search_trains_service(source_id,dest_id,date_obj)
    if error:
        return jsonify({"message":error}),400

    
    try:
        page=int(request.args.get("page",1))
        limit=int(request.args.get("limit",5))
    except ValueError:
        return jsonify({
            "success":False,
            "message":"Invalid Pagination"
        }),400    
    start=(page-1)*limit 
    end=start+limit
    paginated_result=result[start:end] 

    schema=TrainResultSchema(many=True)
    paginated_result=schema.dump(paginated_result)
              
    return jsonify({
        "success":True,
        "data":{
            "page":page,
            "limit":limit,
            "total_results":len(result),
            "data":paginated_result           
        }

     }),200            


#search stations
@search_bp.route("/stations", methods=["GET"])
def search_stations():
    query = request.args.get("query")

    if not query:
        return jsonify({
            "success":False,
            "message":"Query required"
        }),400
    result,_=search_stations_service(query)
    return jsonify({
        "success":True,
        "data":result
    }),200

    