from app.svc.match.playground.consts import TOTAL_CHESS_CNT, CHESSBOARD_HEIGHT, CHESSBOARD_WIDTH
from app.svc.match.playground.chessman import Chessman
from app.svc.match.playground.chess_color import ChessColor
import os


class Chessboard(object):
    def __init__(self, chessmen=None, active_player_color=None):
        if chessmen is None:
            chessmen = [Chessman(i) for i in range(TOTAL_CHESS_CNT)]
        if active_player_color is None:
            active_player_color = ChessColor.RED
        # board[i][j] is corresponding to GlobalPosition(i, j)
        self._board = [
            [None] *
            CHESSBOARD_HEIGHT for j in range(CHESSBOARD_WIDTH)]
        self._chessmen = [None] * TOTAL_CHESS_CNT
        self._active_player_color = active_player_color
        for chessman in chessmen:
            if chessman is None:
                continue
            chess_id = chessman.id
            if self._chessmen[chess_id] is not None:
                raise ValueError(
                    "Two chessmen with identical id {}".format(chess_id))
            self._chessmen[chess_id] = chessman
        for chessman in chessmen:
            if chessman is None:
                continue
            x = chessman.position.x
            y = chessman.position.y
            if self._board[x][y] is not None:
                raise ValueError("Can't assign chessman {} to {} taken by chessman {}".format(
                    chessman, (x, y), self._chessmen[self._board[x][y]]))
            self._board[x][y] = chessman.id

    def __str__(self):
        _EMPTY_SLOT_ = '十'
        _HORIZONTAL_LINE_ = '一'
        _BETWEEN_LINES_ = '丨　' * (CHESSBOARD_WIDTH - 1) + '丨' + os.linesep
        _REVER_ = '丨' + '　' * 15 + '丨' + os.linesep
        board = self._board
        chars = []
        for j in range(CHESSBOARD_HEIGHT - 1, -1, -1):
            for i in range(CHESSBOARD_WIDTH):
                chess_id = board[i][j]
                if chess_id is None:
                    chars.append(_EMPTY_SLOT_)
                else:
                    chars.append(self._chessmen[chess_id].char)
                if i == CHESSBOARD_WIDTH - 1:
                    chars.append(os.linesep)
                else:
                    chars.append(_HORIZONTAL_LINE_)
            if j != 0:
                if j == 5:
                    chars.append(_REVER_)
                else:
                    chars.append(_BETWEEN_LINES_)
        return ''.join(chars)

    @property
    def active_player_color(self):
        return self._active_player_color

    def to_dict(self):
        return {
            'active_player_color': self.active_player_color.value,
            'chessmen': [chessman.to_dict() for chessman in self._chessmen if chessman is not None]
        }

    @staticmethod
    def from_dict(data):
        active_player_color = data['active_player_color']
        chessmen = [Chessman.from_dict(chessman_dict)
                    for chessman_dict in data['chessmen']]
        return Chessboard(chessmen, active_player_color)
