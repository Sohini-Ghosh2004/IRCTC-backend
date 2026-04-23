from app.extensions import db

class User(db.Model):
    __tablename__="users"

    user_id=db.Column(db.Integer,primary_key=True,nullable=False)
    username=db.Column(db.String(100),unique=True,nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password_hash=db.Column(db.String(250),nullable=False)
    role=db.Column(db.String(20),default="user")
    created_at=db.Column(db.DateTime,server_default=db.func.now())