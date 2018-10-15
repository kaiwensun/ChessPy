import uuid
import random
from . import exceptions

_MATCHES = {}
_PRIVATE_PENDING_MATCHES = {}
_PUBLIC_PENDING_MATCHES = set()
_ON_GOING_MATCHES = set()
_USER_2_MATCH = {}


class Match(object):
    def __init__(self, player1_uid, join_token):
        self.player_uids = [player1_uid, None]
        player1_color = random.randint(0, 1)
        colors = ["red", "black"]
        self.player_colors = [colors[player1_color], colors[1 - player1_color]]
        self.match_id = uuid.uuid4().hex
        self.join_token = join_token

    def set_player2(self, player2_uid):
        if self.player_uids[1]:
            raise exceptions.CannotJoinMatchException()
        self.player_uids[1] = player2_uid

    def to_dict(self):
        return {
            'player_uids': self.player_uids,
            'player_colors': self.player_colors,
            'match_id': self.match_id,
            'join_token': self.join_token
        }


def create_match(player1_uid, join_token):
    if player1_uid in _USER_2_MATCH:
        raise exceptions.AlreadyInMatchException()
    if _PUBLIC_PENDING_MATCHES and not join_token:
        return join_match(player1_uid, join_token)
    match = Match(player1_uid, join_token)
    _MATCHES[match.match_id] = match
    if join_token:
        if join_token in _PRIVATE_PENDING_MATCHES:
            raise exceptions.CannotCreateMatchException()
        _PRIVATE_PENDING_MATCHES[join_token] = match.match_id
    else:
        _PUBLIC_PENDING_MATCHES.add(match.match_id)
    _USER_2_MATCH[player1_uid] = match.match_id
    return match


def join_match(player2_uid, join_token):
    if player2_uid in _USER_2_MATCH:
        raise exceptions.AlreadyInMatchException()
    if not _PUBLIC_PENDING_MATCHES and not join_token:
        return create_match(player2_uid, join_token)
    if join_token:
        match_id = _PRIVATE_PENDING_MATCHES.get(join_token)
        if match_id:
            raise exceptions.CannotJoinMatchException()
        match = _MATCHES[match_id]
    else:
        match_id = _PUBLIC_PENDING_MATCHES.pop()
        match = _MATCHES[match_id]
    match.set_player2(player2_uid)
    _USER_2_MATCH[player2_uid] = match.match_id
    _ON_GOING_MATCHES.add(match.match_id)
    return match


def leave_match(player_uid):
    match_id = _USER_2_MATCH.get(player_uid)
    if not match_id:
        return
    match = _MATCHES.pop(match_id)
    if match.player_uids[1] is None:
        if match.join_token:
            del _PRIVATE_PENDING_MATCHES[match_id]
        else:
            _PUBLIC_PENDING_MATCHES.remove(match_id)
    else:
        _ON_GOING_MATCHES.remove(match_id)
        for player_uid in match.player_uids:
            del _USER_2_MATCH[player_uid]


def get_match(match_id):
    return _MATCHES.get(match_id)

# For debug use only


def _get_all_data():
    matches_dict = {
        key: value.to_dict()
        for key, value in _MATCHES.items()
    }
    return {
        '_PRIVATE_PENDING_MATCHES': _PRIVATE_PENDING_MATCHES,
        '_PUBLIC_PENDING_MATCHES': list(_PUBLIC_PENDING_MATCHES),
        '_MATCHES': matches_dict,
        '_USER_2_MATCH': _USER_2_MATCH,
        '_ON_GOING_MATCHES': list(_ON_GOING_MATCHES)
    }
