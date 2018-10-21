from flask import Blueprint
from flask import jsonify
from flask import request
from app.svc.membership import driver as membership_driver
from app.svc.match import driver as match_driver
from app.flask_ext import redis_client

bp = Blueprint(__name__.split('.')[2], __name__)


@bp.route('ping')
def ping():
    return 'OK'


@bp.route('all_users')
def all_users():
    lst = membership_driver.get_all_users(100)
    return jsonify({'users': [user._to_dict() for user in lst]})


@bp.route('all_matches')
def all_matches():
    match_data = match_driver._get_all_data()
    return jsonify(match_data)


@bp.route('clear_redis')
def clear_redis():
    redis_client.flushdb()
    return "redis data is cleaned."
