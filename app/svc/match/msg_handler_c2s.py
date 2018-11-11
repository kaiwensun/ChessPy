import json

from flask_login import current_user

from app.svc.match.msg_meta import *
from app.svc.match import driver as match_driver
from app.svc.match.match_db import MatchDB
from app.svc.match.playground.chessman import Chessman


def handle_c2s(message):
    handlers = {
        MSG_TYPE_CHESSMOVE: handle_chessmove,
        MSG_TYPE_HEARTBEAT: handle_heartbeat,
        MSG_TYPE_UNDOREQ: handle_undo_request,
        MSG_TYPE_REPLYUNDOREQ: handle_reply_undo_request
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
    another_uid = match.another_player_uid
    another_user_is_online = MatchDB.get('HEART_BEAT', another_uid, ex=None)
    return {'another': another_user_is_online}


def handle_undo_request(message):
    match = match_driver.get_match(current_user.user_id)
    chessboard = match.chessboard
    if not chessboard or not chessboard.can_undo():
        return {'result': False}
    # If your undo request within the past 60s was not approved, by the ohter
    # player, then you can't request again.
    can_request = MatchDB.set(
        'undoreq',
        "{}-{}".format(current_user.user_id, match.match_id),
        'requesting',
        nx=True,
        ex=60)
    if not can_request:
        return {'result': False}
    msg_type = message['msg_type']
    msg_data = message['msg_data']
    match.send_message_from(current_user.user_id, msg_type, msg_data)
    return {'result': True}


def handle_reply_undo_request(message):
    msg_data = json.loads(message['msg_data'])
    match = match_driver.get_match(current_user.user_id)
    if not msg_data or not msg_data.get('approved'):
        msg_data = {'approved': False}
        match.send_message_from(
            current_user.user_id,
            MSG_TYPE_REPLYUNDOREQ,
            msg_data)
        return msg_data
    try:
        lock, chessboard = match.lock_and_get_chessboard()
        if not chessboard:
            match.send_message_from(
                current_user.user_id,
                MSG_TYPE_REPLYUNDOREQ,
                msg_data)
            return msg_data
        step = chessboard.undo()
        if not step:
            match.send_message_from(
                current_user.user_id,
                MSG_TYPE_REPLYUNDOREQ,
                msg_data)
            return msg_data
        match.chessboard = chessboard
        step['undone_color'] = Chessman.id2color(step['chess_id']).value
        kill_chess_id = step['kill_chess_id']
        if kill_chess_id is not None:
            killed_color = Chessman.id2color(kill_chess_id)
            step['killed_color'] = killed_color.value
            step['killed_char'] = Chessman.role2char(
                Chessman.id2role(kill_chess_id),
                color=killed_color)
        msg_data = {'approved': True,
                    'step': step}
        match.send_message_from(
            current_user.user_id,
            MSG_TYPE_REPLYUNDOREQ,
            msg_data)
        return msg_data
    finally:
        MatchDB.delete(
            'undoreq',
            "{}-{}".format(match.another_player_uid, match.match_id))
        lock.release()
