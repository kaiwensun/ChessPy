from app.flask_ext import redis_client

from redis_collections import Dict
from app.svc.match import exceptions, msg_meta
from app.svc.match.playground.chessboard import Chessboard
from app.svc.match.match import Match
from app.svc.match.match_db import MatchDB
from app.shared import utils
from config import settings

_ALL_MATCHES = Dict(key="ALL_MATCHES", redis=redis_client)
_USER_2_MATCH_ID = Dict(key="USER_2_MATCH_ID", redis=redis_client)
_PRIVATE_PENDING_MATCH_IDS = 'private_pending_match_ids'
_PUBLIC_PENDING_MATCH_IDS = 'public_pending_match_ids'


def _lock(typ, key, blocking=False):
    lock_id = 'lock-{}-{}'.format(typ, key)
    print("locking {}.".format(lock_id))
    lock = redis_client.lock(lock_id)
    acquired = lock.acquire(blocking=blocking)
    print("{} to acquire lock {}".format(
        'succeed' if acquired else 'failed', lock_id))
    return lock, acquired


def join_match(player_uid, join_token):
    _register_player(player_uid, bool(join_token))
    try:
        if join_token:
            match_lock, _ = _lock('join_token', join_token)
            match_id = MatchDB.takeaway(_PRIVATE_PENDING_MATCH_IDS, join_token)
        else:
            match_id = MatchDB.dequeue(_PUBLIC_PENDING_MATCH_IDS, None, False)
        if match_id is None:
            return _create_match(player_uid, join_token)
        else:
            all_match_lock, _ = _lock('all_match', match_id)
    finally:
        if join_token:
            match_lock.release()
    try:
        match = _ALL_MATCHES[match_id]
        match.set_player2(player_uid)
        _ALL_MATCHES[match_id] = match
        _USER_2_MATCH_ID[player_uid] = match.match_id
        chessboard = Chessboard()
        redis_client.setex(
            match.chessboard_id,
            settings.GAME_TTL,
            chessboard.to_dict())
        return match
    finally:
        all_match_lock.release()


def _create_match(player_uid1, join_token):
    match = Match(player_uid1, join_token)
    _USER_2_MATCH_ID[player_uid1] = match.match_id
    if join_token:
        MatchDB.set(_PRIVATE_PENDING_MATCH_IDS, join_token, match.match_id)
    else:
        MatchDB.enqueue(_PUBLIC_PENDING_MATCH_IDS, None, match.match_id)
    _ALL_MATCHES[match.match_id] = match
    return match


def leave_match(player_uid):
    match_id = _USER_2_MATCH_ID.pop(player_uid, None)
    if not match_id:
        return
    try:
        all_match_lock, _ = _lock('all_match', match_id)
        match = _ALL_MATCHES.get(match_id)
        if not match:
            return
        if match.active_players_cnt == 2:
            match.remove_player(player_uid)
            _ALL_MATCHES[match_id] = match
            message = {
                'type': msg_meta.MSG_TYPE_CONTROL,
                'data': msg_meta.MSG_CONST_LEFT
            }
            match.send_message_from(player_uid, message)
            return
        match = _ALL_MATCHES.pop(match_id)
        if match.join_token:
            MatchDB.delete(_PRIVATE_PENDING_MATCH_IDS, match.join_token)
        else:
            MatchDB.force_remove_from_queue(
                _PUBLIC_PENDING_MATCH_IDS, None, match_id)
        redis_client.delete(match.chessboard_id)
    finally:
        all_match_lock.release()


def get_match(player_uid):
    match_id = _USER_2_MATCH_ID.get(player_uid)
    if not match_id:
        return exceptions.NoMatchFoundException()
    return _ALL_MATCHES.get(match_id, None)


def _register_player(user_id, is_public_game):
    register_lock = redis_client.lock('register_user-{}'.format(user_id))
    if not register_lock.acquire(blocking=False):
        raise exceptions.AlreadyInMatchException()
    try:
        if not _USER_2_MATCH_ID.get(user_id):
            _USER_2_MATCH_ID[user_id] = is_public_game
        else:
            raise exceptions.AlreadyInMatchException()
    finally:
        register_lock.release()


@utils.not_on_production
def _get_all_data():
    all_matches = _ALL_MATCHES._data()
    all_matches = {key: value.to_dict() for key, value in all_matches.items()}
    return {
        '_ALL_MATCHES': all_matches,
        '_USER_2_MATCH_ID': _USER_2_MATCH_ID._data(),
        '_PRIVATE_PENDING_MATCH_IDS':
            MatchDB.dump_table(_PRIVATE_PENDING_MATCH_IDS),
        '_PUBLIC_PENDING_MATCH_ID':
            MatchDB.get_queue(_PUBLIC_PENDING_MATCH_IDS, None)
    }
