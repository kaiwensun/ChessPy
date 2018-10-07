from flask import Blueprint, render_template

bp = Blueprint(__name__.split('.')[2], __name__)

@bp.route('/')
def index():
    return render_template('game/index.html')
