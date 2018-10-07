from flask import Blueprint

bp = Blueprint(__name__.split('.')[2], __name__)


@bp.route('ping')
def pint():
    return 'OK'
