import os

from flask import Flask
from config import settings

from app.views.home.views import bp as home_bp
from app.views.control.views import bp as control_bp
from app.shared import utils

os.environ['FLASK_ENV'] = settings.ENV

app = Flask(__name__)
app.register_blueprint(home_bp, url_prefix='/home')
app.register_blueprint(control_bp, url_prefix='/control')

app.jinja_env.globals.update(utils=utils)
