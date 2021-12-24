from extension import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String, default="user")
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_last_updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

