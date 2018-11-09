import uuid
import random

from flask_login import current_user

from app.flask_ext import redis_client
from app.svc.match.playground.chess_color import ChessColor
from app.svc.match.playground.chessboard import Chessboard
from app.svc.match.match_db import MatchDB
from app.svc.match import msg_meta
from app.svc.match import exceptions
from app.svc.match import driver as match_driver


class Match(object):
    def __init__(self, player1_uid, join_token):
        self._match_id = '{}-{}'.format('private' if join_token else 'public',
                                        uuid.uuid4().hex)
        self._player_uids = [player1_uid, None]
        player1_color = random.randint(0, 1)
        colors = [ChessColor.RED, ChessColor.BLACK]
        self._player_colors = [
            colors[player1_color], colors[1 - player1_color]]
        self._join_token = join_token

    def set_player2(self, player2_uid):
        self._player_uids[1] = player2_uid

    def remove_player(self, player_uid):
        self._player_uids = [
            puid if puid != player_uid else None for puid in self._player_uids]

    @property
    def match_id(self):
        return self._match_id

    @property
    def player_uids(self):
        return self._player_uids.copy()

    @property
    def player_colors(self):
        return self._player_colors

    @property
    def join_token(self):
        return self._join_token

    @property
    def player_color(self):
        player_index = self.player_uids.index(current_user.user_id)
        return self.player_colors[player_index]

    def to_dict(self):
        return {
            'player_uids': self.player_uids,
            'player_colors': [color.value for color in self.player_colors],
            'match_id': self.match_id,
            'join_token': self.join_token
        }

    @staticmethod
    def from_dict(data):
        if data is None:
            return None
        match = Match(data['player_uids'][0], data['join_token'])
        match._player_uids[1] = data['player_uids'][1]
        match._player_colors = [ChessColor(color)
                                for color in data['player_colors']]
        match._match_id = data['match_id']
        return match

    def _channel_to(self, player_uid):
        if not all(self.player_uids):
            return None
        if self.player_uids[1] == player_uid:
            from_uid, to_uid = self.player_uids
        elif self.player_uids[0] == player_uid:
            to_uid, from_uid = self.player_uids
        else:
            return None
        return '{}-{}'.format(from_uid, to_uid)

    def send_message_from(self, my_uid, msg_type, msg_data):
        for other_uid in self.player_uids:
            if other_uid != my_uid:
                channel_name = self._channel_to(other_uid)
        message = {
            'msg_type': msg_type,
            'msg_data': msg_data
        }
        MatchDB.enqueue('match_channel', channel_name, message)

    def receive_message_to(self, my_uid):
        channel_name = self._channel_to(my_uid)
        message = MatchDB.dequeue('match_channel', channel_name, False)
        return message or {
            'msg_type': msg_meta.MSG_TYPE_NOP,
            'msg_data': None
        }

    def move(self, src, dst):
        player_color = self.player_color
        chessboard = self.chessboard
        if player_color != chessboard.active_player_color:
            raise exceptions.NotYourTurn()
        chessboard.move(src[0], src[1], dst[0], dst[1])
        self.chessboard = chessboard

    @property
    def active_players_cnt(self):
        return len([puid for puid in self.player_uids if puid])

    @property
    def chessboard_id(self):
        return "chessboard-{}".format(self.match_id)

    @property
    def chessboard(self):
        return match_driver.get_chessboard(self.chessboard_id)

    @chessboard.setter
    def chessboard(self, value):
        match_driver.set_chessboard(self.chessboard_id, value)
