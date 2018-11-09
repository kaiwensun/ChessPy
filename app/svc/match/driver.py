from app.flask_ext import redis_client

from redis_collections import Dict
from app.svc.match import exceptions, msg_meta
from app.svc.match.playground.chessboard import Chessboard
from app.svc.match.match import Match
from app.svc.match.match_db import MatchDB
from app.shared import utils
from config import settings

_ALL_MATCHES = "all_matches"
_USER_2_MATCH_ID = "user_2_match_id"
_PRIVATE_PENDING_MATCH_IDS = 'private_pending_match_ids'
_PUBLIC_PENDING_MATCH_IDS = 'public_pending_match_ids'
_CHESSBOARD = 'chessboard'


def _lock(typ, key, blocking=False):
    lock_id = 'lock-{}-{}'.format(typ, key)
    print("locking {}.".format(lock_id))
    lock = redis_client.lock(lock_id)
    acquired = lock.acquire(blocking=blocking)
    print("{} to acquire lock {}".format(
        'succeed' if acquired else 'failed', lock_id))
    return lock, acquired


def join_match(player_uid, join_token):
    try:
        _register_player(player_uid, bool(join_token))
    except exceptions.AlreadyInMatchException:
        match_id = MatchDB.get(_USER_2_MATCH_ID, player_uid)
        return Match.from_dict(MatchDB.get(_ALL_MATCHES, match_id))
    try:
        if join_token:
            blocking_timeout = min(settings.GAME_TTL // 2, 5)
            match_room_door, can_use_door = MatchDB.lock(
                'match_room_door',
                join_token,
                blocking_timeout=blocking_timeout)
            if not can_use_door:
                raise exceptions.CannotAcquireMatchDoor(
                    'the door {} is too crowded.'.format(join_token))
            population = MatchDB.enter_private_match(join_token)
            if population == 1:
                # going to create a match
                match_id = None
            elif population == 2:
                # going to join an existing match
                match_id = MatchDB.takeaway(
                    _PRIVATE_PENDING_MATCH_IDS, join_token)
            elif population > 2:
                # join_token collisioni. try another join_token
                raise exceptions.InvalidMatchState(
                    'join_token {} is already in use by at least 2 players.'
                    .format(join_token))
        else:
            match_id = MatchDB.dequeue(_PUBLIC_PENDING_MATCH_IDS, None, False)
        if match_id is None:
            match = _create_match(player_uid, join_token)
        else:
            match = Match.from_dict(MatchDB.get(_ALL_MATCHES, match_id))
            match.set_player2(player_uid)
            MatchDB.set(_USER_2_MATCH_ID, player_uid, match.match_id)
            MatchDB.set(_ALL_MATCHES, match_id, match.to_dict())
        match.send_message_from(
            player_uid,
            msg_meta.MSG_TYPE_CONTROL,
            msg_meta.MSG_CONST_JOIN)
        return match
    finally:
        if join_token:
            match_room_door.release()


def _create_match(player_uid1, join_token):
    match = Match(player_uid1, join_token)
    success = MatchDB.set(
        _USER_2_MATCH_ID,
        player_uid1,
        match.match_id,
        xx=True)
    if not success:
        raise ValueError(
            'player {} should register before creating a match'
            .format(player_uid1))
    if join_token:
        success = MatchDB.set(
            _PRIVATE_PENDING_MATCH_IDS,
            join_token,
            match.match_id,
            nx=True)
        if not success:
            raise exceptions.InvalidMatchState(
                'join_token {} is already in use by at least 2 players.'
                .format(join_token))
    else:
        MatchDB.enqueue(_PUBLIC_PENDING_MATCH_IDS, None, match.match_id)
    success = MatchDB.set(
        _ALL_MATCHES,
        match.match_id,
        match.to_dict(),
        nx=True)
    if not success:
        raise exceptions.InvalidMatchState(
            'Match {} is already created'.format(
                match.match_id))
    chessboard = Chessboard()
    MatchDB.set(_CHESSBOARD, match.chessboard_id, chessboard.to_dict())
    return match


def leave_match(player_uid):
    blocking_timeout = min(settings.GAME_TTL // 2, 5)
    match_id = MatchDB.takeaway(_USER_2_MATCH_ID, player_uid)
    if not match_id:
        raise exceptions.InvalidMatchState(
            "Can't find the match_id for user {}.".format(player_uid))
    try:
        join_token = None
        match = Match.from_dict(MatchDB.get(_ALL_MATCHES, match_id))
        if not match:
            raise exceptions.InvalidMatchState(
                "Can't find the match {} to leave.".format(match_id))
        join_token = match.join_token
        if join_token:
            match_room_door, can_use_door = MatchDB.lock(
                'match_room_door',
                join_token,
                blocking_timeout=blocking_timeout)
            if not can_use_door:
                raise exceptions.CannotAcquireMatchDoor(
                    'the door {} is too crowded.'.format(join_token))

        match.remove_player(player_uid)
        if match.active_players_cnt == 1:
            match.send_message_from(
                player_uid,
                msg_meta.MSG_TYPE_CONTROL,
                msg_meta.MSG_CONST_LEFT)
            MatchDB.set(_ALL_MATCHES, match.match_id, match.to_dict())
            return
        # the last one leaving the match should clean up the mess
        match = MatchDB.takeaway(_ALL_MATCHES, match_id)
        if match.join_token:
            MatchDB.delete(_PRIVATE_PENDING_MATCH_IDS, match.join_token)
        else:
            MatchDB.force_remove_from_queue(
                _PUBLIC_PENDING_MATCH_IDS, None, match_id)
        MatchDB.delete(_CHESSBOARD, match.chessboard_id)
    finally:
        if join_token:
            match_room_door.release()


def get_match(player_uid):
    match_id = MatchDB.get(_USER_2_MATCH_ID, player_uid)
    if not match_id:
        raise exceptions.NoMatchFoundException()
    return Match.from_dict(MatchDB.get(_ALL_MATCHES, match_id))


def get_chessboard(chessboard_id):
    return Chessboard.from_dict(MatchDB.get(_CHESSBOARD, chessboard_id))


def set_chessboard(chessboard_id, chessboard):
    return MatchDB.set(_CHESSBOARD, chessboard_id, chessboard.to_dict())


def _register_player(user_id, is_public_game):
    success = MatchDB.set(_USER_2_MATCH_ID, user_id, is_public_game, nx=True)
    if not success:
        raise exceptions.AlreadyInMatchException()


@utils.not_on_production
def _get_all_data():
    return {
        '_ALL_MATCHES': MatchDB.dump_table(_ALL_MATCHES),
        '_USER_2_MATCH_ID':
            MatchDB.dump_table(_USER_2_MATCH_ID),
        '_PRIVATE_PENDING_MATCH_IDS':
            MatchDB.dump_table(_PRIVATE_PENDING_MATCH_IDS),
        '_PUBLIC_PENDING_MATCH_ID':
            MatchDB.get_queue(_PUBLIC_PENDING_MATCH_IDS, None)
    }
