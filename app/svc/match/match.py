import uuid
import random

from app.flask_ext import redis_client
from app.svc.match.playground.chess_color import ChessColor
from app.svc.match.match_db import MatchDB


class Match(object):
    def __init__(self, player1_uid, join_token):
        self._match_id = '{}-{}'.format('private' if join_token else 'public',
                                        uuid.uuid4().hex)
        self.player_uids = [player1_uid, None]
        player1_color = random.randint(0, 1)
        colors = [ChessColor.RED, ChessColor.BLACK]
        self._player_colors = [
            colors[player1_color], colors[1 - player1_color]]
        self._join_token = join_token

    def set_player2(self, player2_uid):
        self.player_uids[1] = player2_uid

    def remove_player(self, player_uid):
        self.player_uids = [
            puid if puid != player_uid else None for puid in self.player_uids]

    @property
    def match_id(self):
        return self._match_id

    @property
    def player_colors(self):
        return self._player_colors

    @property
    def join_token(self):
        return self._join_token

    def to_dict(self):
        return {
            'player_uids': self.player_uids,
            'player_colors': self.player_colors,
            'match_id': self.match_id,
            'join_token': self.join_token
        }

    @staticmethod
    def from_dict(data):
        match = Match(data['player_uids'][0], data['join_token'])
        match._match_id = data['match_id']
        match._join_token = data['join_token']
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

    def send_message_from(self, my_uid, message):
        for other_uid in self.player_uids:
            if other_uid != my_uid:
                channel_name = self._channel_to(other_uid)
        MatchDB.enqueue('match_channel', channel_name, message)

    def receive_message_to(self, my_uid):
        channel_name = self._channel_to(my_uid)
        return MatchDB.dequeue('match_channel', channel_name, False)

    @property
    def active_players_cnt(self):
        return len([puid for puid in self.player_uids if puid])

    @property
    def chessboard_id(self):
        return "chessboard-{}".format(self.match_id)
