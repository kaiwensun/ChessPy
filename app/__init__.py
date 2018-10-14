import os

from flask import Flask
from flask import request

from app.views.site.views import bp as site_bp
from app.views.control.views import bp as control_bp
from app.views.modals.views import bp as modals_bp
from app.views.membership.views import bp as membership_bp

from app.svc.membership import driver as membership_driver
from app.flask_ext import db, login_manager, csrf

from app.shared import utils
from config import settings


os.environ['FLASK_ENV'] = settings.ENV

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.FLASK_APP_SECRET_KEY

# Blueprints
app.register_blueprint(site_bp, url_prefix='/')
app.register_blueprint(control_bp, url_prefix='/control')
app.register_blueprint(modals_bp, url_prefix='/modals')
app.register_blueprint(membership_bp, url_prefix='/membership')

# Global variable
app.add_template_global(name="utils", f=utils)

# Login manager
login_manager.user_loader(membership_driver.get_user_by_alternative_id)
login_manager.init_app(app)

# Flask-WTF CSRF
csrf.init_app(app)


# SQL Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../DB/database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# class students(db.Model):
#    id = db.Column('student_id', db.Integer, primary_key = True)
#    name = db.Column(db.String(100))
#    city = db.Column(db.String(50))
#    addr = db.Column(db.String(200))
#    pin = db.Column(db.String(10))

with app.app_context():
    db.create_all()
