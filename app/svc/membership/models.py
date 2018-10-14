from app.flask_ext import db


class User(db.Model):
    user_id = db.Column(db.String(32), primary_key=True, nullable=False)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    hashed_pw = db.Column(db.String(64), nullable=False)
    pw_created_at = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.String(20), nullable=False)
