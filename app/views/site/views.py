from flask import Blueprint, render_template

bp = Blueprint(__name__.split('.')[2], __name__)


@bp.route('/')
def index():
    return render_template('site/index.html')


@bp.route('/play')
def play():
    return render_template('site/play.html')
