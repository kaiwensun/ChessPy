import json

from flask_login import current_user

from app.svc.match.msg_meta import *
from app.svc.match import driver as match_driver
from app.svc.match.match_db import MatchDB


def handle_c2s(message):
    handlers = {
        MSG_TYPE_CHESSMOVE: handle_chessmove,
        MSG_TYPE_HEARTBEAT: handle_heartbeat
    }
    handler = handlers.get(message['msg_type'])
    return handler(message)


def handle_chessmove(message):
    msg_type = message['msg_type']
    msg_data = json.loads(message['msg_data'])
    match = match_driver.get_match(current_user.user_id)
    match.move(msg_data['src'], msg_data['dst'])
    match.send_message_from(current_user.user_id, msg_type, msg_data)
    return {'chessboard': str(match.chessboard)}


def handle_heartbeat(message):
    MatchDB.set('HEART_BEAT', current_user.user_id, True, ex=5)
    match = match_driver.get_match(current_user.user_id)
    another_uid = [
        uid for uid in match.player_uids if uid != current_user.user_id][0]
    another_user_is_online = MatchDB.get('HEART_BEAT', another_uid, ex=None)
    return {'another': another_user_is_online}
