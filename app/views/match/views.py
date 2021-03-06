import json
import time
import datetime

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import session
from flask import redirect
from flask import url_for
from flask import render_template
from flask import Response
from flask import stream_with_context
from flask_login import current_user

from . import forms
from app.svc.match.msg_handler_c2s import handle_c2s
from app.svc.match.msg_handler_s2c import handle_s2c, force_to_stop
from app.svc.match.msg_meta import MSG_TYPE_NOP
from app.svc.match import exceptions

from app.svc.membership import driver as membership_driver
from app.svc.match import driver as match_driver
from config import settings

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
    return redirect(url_for('match.view_match'))


@bp.route('join_public_match', methods=['POST'])
def join_public_match():
    form = forms.JoinPublicMatchForm()
    if not form.validate_on_submit():
        return 'error 1'
    match = match_driver.join_match(
        current_user.user_id, None)
    if not match:
        return 'error 2'
    return redirect(url_for('match.view_match'))


@bp.route('view_match')
def view_match():
    try:
        match = match_driver.get_match(current_user.user_id)
    except exceptions.NoMatchFoundException:
        return redirect(url_for('site.index'))
    match_msg_form = forms.MessageForm()
    return render_template('site/play.html', match=match,
                           OFFLINE_TTL=settings.OFFLINE_TTL,
                           match_msg_form=match_msg_form)


@bp.route('receive_match_message')
def receive_match_message():
    def yield_message():
        last_valid_msg_time = datetime.datetime.now()
        while True:
            rval = handle_s2c()
            if rval is None:
                break
            print(rval['msg_type'])
            if rval['msg_type'] != MSG_TYPE_NOP:
                last_valid_msg_time = datetime.datetime.now()
                yield 'data: {}\n\n'.format(json.dumps(rval))
            else:
                now = datetime.datetime.now()
                delta = (now - last_valid_msg_time).seconds
                if delta > settings.OFFLINE_TTL:
                    # offline too long. force match to stop
                    force_to_stop()
                    break
                if delta > 5:
                    yield 'data: {}\n\n'.format(json.dumps(rval))
                time.sleep(0.5)
    return Response(stream_with_context(yield_message()),
                    mimetype='text/event-stream')


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
