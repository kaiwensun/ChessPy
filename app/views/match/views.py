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


@bp.route('join_match', methods=['POST'])
def create_match():
    form = forms.CreateMatchForm()
    if not form.validate_on_submit():
        return 'error 1'
    match = match_driver.join_match(
        current_user.user_id, form.join_token.data)
    if not match:
        return 'error 2'
    return redirect(url_for('match.view_match',
                            player_uid=current_user.user_id))


@bp.route('view_match')
def view_match():
    match = match_driver.get_match(request.args.get('player_uid'))
    if match and current_user.user_id in match.player_uids:
        return jsonify(match.to_dict())
    else:
        return 'error'
