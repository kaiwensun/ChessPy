from flask_login import current_user

from app.svc.match.match_db import MatchDB
from app.svc.match import driver as match_driver
from app.svc.match.msg_meta import MSG_TYPE_MATCHEND
from app.svc.match import exceptions


def handle_s2c():
    try:
        match = match_driver.get_match(current_user.user_id)
    except exceptions.NoMatchFoundException:
        return None
    message = match.receive_message_to(current_user.user_id)
    handlers = {
        MSG_TYPE_MATCHEND: handle_matchend
    }
    msg_handler = handlers.get(message['msg_type'])
    if msg_handler:
        msg_handler(message)
    print("handle_s2c to {}: {}".format(current_user.user_id, message))
    return message


def handle_matchend(message):
    match_driver.leave_match(current_user.user_id)


def force_to_stop():
    match = match_driver.get_match(current_user.user_id)
    if match.is_over:
        return {'result': False}
    msg_type = MSG_TYPE_MATCHEND
    msg_data = {'winner': match.player_color,
                'reason': 'offline'}
    for player_uid in match.player_uids:
        match.send_message_from(player_uid, msg_type, msg_data)
    return {'result': True}
