from flask import Blueprint, render_template
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
