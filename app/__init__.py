import os

from flask import Flask
from flask import request

from app.views.game.views import bp as game_bp
from app.views.control.views import bp as control_bp
from app.views.modals.views import bp as modals_bp
from app.shared import utils
from config import settings


# from flask_sqlalchemy import SQLAlchemy


os.environ['FLASK_ENV'] = settings.ENV

app = Flask(__name__)

app.register_blueprint(game_bp, url_prefix='/game')
app.register_blueprint(control_bp, url_prefix='/control')
app.register_blueprint(modals_bp, url_prefix='/modals')

app.add_template_global(name="utils", f=utils)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/database.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# class students(db.Model):
#    id = db.Column('student_id', db.Integer, primary_key = True)
#    name = db.Column(db.String(100))
#    city = db.Column(db.String(50))
#    addr = db.Column(db.String(200))
#    pin = db.Column(db.String(10))


# db.create_all()
