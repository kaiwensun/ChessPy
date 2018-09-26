from flask import Blueprint

bp = Blueprint(__name__, __name__)

@bp.route('ping')
def pint():
    return 'OK'
