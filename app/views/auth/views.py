from flask import Blueprint

bp = Blueprint(__name__.split('.')[2], __name__)


@bp.route('sign-up', methods=['POST'])
def sign_up():
    return 'OK'
