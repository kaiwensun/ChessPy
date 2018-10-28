from flask import Blueprint
from flask import request
from flask import jsonify
from flask import session
from flask import redirect
from flask import url_for
from flask_login import current_user

from . import forms

from app.svc.membership import driver as membership_driver
from app.svc.match import driver as match_driver

bp = Blueprint(__name__.split('.')[2], __name__)


@bp.route('join_private_match', methods=['POST'])
def join_private_match():
    form = forms.JoinPrivateMatchForm()
    if not form.validate_on_submit():
        return 'error 1'
    match = match_driver.join_match(
        current_user.user_id, form.join_token.data)
    if not match:
        return 'error 2'
    return jsonify(match.to_dict())


@bp.route('join_public_match', methods=['POST'])
def join_public_match():
    form = forms.JoinPublicMatchForm()
    if not form.validate_on_submit():
        return 'error 1'
    match = match_driver.join_match(
        current_user.user_id, None)
    if not match:
        return 'error 2'
    return jsonify(match.to_dict())


@bp.route('view_match')
def view_match():
    match = match_driver.get_match(request.args.get('player_uid'))
    if match and current_user.user_id in match.player_uids:
        return jsonify(match.to_dict())
    else:
        return 'error'
