from flask import Blueprint
from flask import request
from flask import jsonify
from flask import session
from flask import redirect
from flask import url_for
from flask import render_template
from flask_login import current_user

from . import forms
from app.svc.match.msg_handler_c2s import handle_c2s
from app.svc.match.msg_handler_s2c import handle_s2c

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
    match_msg_form = forms.MessageForm()
    return render_template('site/play.html', match=match,
                           match_msg_form=match_msg_form)


@bp.route('view_match')
def view_match():
    match = match_driver.get_match(current_user.user_id)
    if match:
        return jsonify(match.to_dict())
    else:
        return 'error'


@bp.route('receive_match_message')
def receive_match_message():
    return jsonify(handle_s2c())


@bp.route('send_match_message', methods=['POST'])
def send_match_message():
    form = forms.MessageForm()
    if not form.validate():
        return 'error'
    message = {
        'msg_type': form.msg_type.data,
        'msg_data': form.msg_data.data
    }
    return jsonify(handle_c2s(message))
