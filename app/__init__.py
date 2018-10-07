import os

from flask import Flask
from config import settings

from app.views.game.views import bp as game_bp
from app.views.control.views import bp as control_bp
from app.views.modals.views import bp as modals_bp
from app.shared import utils

os.environ['FLASK_ENV'] = settings.ENV

app = Flask(__name__)
app.register_blueprint(game_bp, url_prefix='/game')
app.register_blueprint(control_bp, url_prefix='/control')
app.register_blueprint(modals_bp, url_prefix='/modals')

app.jinja_env.globals.update(utils=utils)
