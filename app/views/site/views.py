import os
from flask import send_from_directory
from flask import Blueprint, render_template
from flask import current_app
from app.views.match.forms import CreateMatchForm

bp = Blueprint(__name__.split('.')[2], __name__)


@bp.route('/')
def index():
    create_match_form = CreateMatchForm()
    return render_template('site/index.html',
                           create_match_form=create_match_form)


@bp.route('/play')
def play():
    return render_template('site/play.html')


@bp.route('/favicon.ico')
def favicon():
    import pdb
    pdb.set_trace()
    return send_from_directory(
        os.path.join(current_app.root_path, 'static', 'images'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')
