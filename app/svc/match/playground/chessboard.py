from app.svc.match.playground.consts import TOTAL_CHESS_CNT, \
    CHESSBOARD_HEIGHT, CHESSBOARD_WIDTH
from app.svc.match.playground.chessman import Chessman
from app.svc.match.playground.position import GlobalPosition
from app.svc.match.playground.chess_color import ChessColor
from app.svc.match.playground.move_history import MoveHistory
import os


class Chessboard(object):
    def __init__(
            self,
            chessmen=[Chessman(i) for i in range(TOTAL_CHESS_CNT)],
            active_player_color=ChessColor.RED,
            move_history=MoveHistory()):
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
                raise ValueError(
                    "Can't assign chessman {} to {} taken by chessman {}"
                    .format(
                        chessman, (x, y), self._chessmen[self._board[x][y]]))
            self._board[x][y] = chessman.id
        self._move_history = move_history

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

    def get_position(self, chess_id):
        chessman = self._chessmen[chess_id]
        if chessman:
            if chessman.id != chess_id:
                raise ValueError(
                    "chessman.id = {}, chess_id = {}".format(
                        chessman.id, chess_id))
            return chessman.position
        return None

    def get_chessman(self, position):
        if isinstance(position, GlobalPosition):
            position = (position.x, position.y)
        chess_id = self._board[position[0]][position[1]]
        if chess_id is not None:
            return self._chessmen[chess_id]
        return None

    def pick_up(self, chess_id):
        chessman = self._chessmen[chess_id]
        position = chessman.position
        chessman.position = None
        assert(self._board[position.x][position.y] == chess_id)
        self._board[position.x][position.y] = None

    def kill(self, chess_id):
        self.pick_up(chess_id)
        self._chessmen[chess_id] = None

    def put_at(self, chess_id, position):
        assert(self.get_chessman(position) is None)
        self._board[position.x][position.y] = chess_id
        chessman = self._chessmen[chess_id]
        if not chessman:
            chessman = Chessman(chess_id)
            self._chessmen[chess_id] = chessman
        chessman.position = position

    def _change_active_player(self):
        if self._active_player_color == ChessColor.BLACK:
            self._active_player_color = ChessColor.RED
        else:
            self._active_player_color = ChessColor.BLACK

    def move(self, src_x, src_y, dst_x, dst_y):
        if self._game_is_over():
            raise ValueError('Game is over')
        src = GlobalPosition(src_x, src_y)
        chessman = self.get_chessman(src)
        if not chessman:
            raise ValueError(
                'Chess is not on board ({})'.format(src))
        chess_id = chessman.id
        if chessman.color != self.active_player_color:
            raise ValueError(
                "{} player can't play {} chess (chess_id={})".format(
                    self.active_player_color, chessman.color, chess_id))
        dst = GlobalPosition(dst_x, dst_y)
        if chessman.can_exist_at(dst) and chessman.can_reach(dst, self):
            target = self.get_chessman(dst)
            if target:
                self.kill(target.id)
            self.pick_up(chess_id)
            self.put_at(chess_id, dst)
            self._change_active_player()
            self._move_history.move(chess_id, src, dst, target and target.id)
            return target
        else:
            raise ValueError(
                "Can't move {} from {} to {}".format(
                    chessman, src, dst))

    def undo(self):
        if not self.can_undo():
            return None
        step = self._move_history.retract()
        chess_id = step['chess_id']
        from_posi = GlobalPosition(
            step['from_posi']['x'],
            step['from_posi']['y'])
        self.pick_up(chess_id)
        self.put_at(chess_id, from_posi)
        kill_chess_id = step['kill_chess_id']
        if kill_chess_id is not None:
            to_posi = GlobalPosition(
                step['to_posi']['x'], step['to_posi']['y'])
            self.put_at(kill_chess_id, to_posi)
        self._change_active_player()
        return step

    def can_undo(self):
        if len(self._move_history) == 0 or self.game_is_over():
            return False
        move_step = self._move_history[-1]
        chess_id = move_step['chess_id']
        if Chessman.id2color(chess_id) == self.active_player_color:
            return False
        return True

    def _game_is_over(self):
        # 15 and 31 are chess_id of the two SHUAI (kings)
        return not bool(self._chessmen[15] and self._chessmen[31])

    @property
    def active_player_color(self):
        return self._active_player_color

    def to_dict(self):
        return {
            'active_player_color': self.active_player_color.value,
            'chessmen': [chessman.to_dict() for chessman in self._chessmen
                         if chessman is not None],
            'move_history': self._move_history.to_dict()
        }

    @staticmethod
    def from_dict(data):
        if data is None:
            return None
        active_player_color = ChessColor(data['active_player_color'])
        chessmen = [Chessman.from_dict(chessman_dict)
                    for chessman_dict in data['chessmen']]
        move_history = MoveHistory.from_dict(data['move_history'])
        return Chessboard(chessmen, active_player_color, move_history)
