from flask import Flask
from app.extensions import db,jwt
from app.config import Config
from app.routes.auth_routes import auth_bp
from app.routes.admin_routes import admin_bp
from app.routes.station_routes import station_bp
from app.routes.train_routes import train_bp
from app.routes.booking_routes import booking_bp
from app.routes.train_schedule_routes import train_schedule_bp
from app.routes.train_stop_routes import train_stop_bp
from app.routes.search_route import search_bp
def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp,url_prefix="/api/auth")
    app.register_blueprint(admin_bp,url_prefix="/api/admin")
    app.register_blueprint(station_bp,url_prefix="/api/stations")
    app.register_blueprint(train_bp,url_prefix="/api/trains")
    app.register_blueprint(train_schedule_bp,url_prefix="/api/train_schedules")
    app.register_blueprint(booking_bp,url_prefix="/api/bookings")
    app.register_blueprint(train_stop_bp,url_prefix="/api/train_stops")
    app.register_blueprint(search_bp,url_prefix="/api/search")
    return app