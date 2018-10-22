from app.svc.match.playground.chess_color import ChessColor
from app.svc.match.playground.chess_role import ChessRole
from app.svc.match.playground.position import GlobalPosition
from app.svc.match.playground.consts import TOTAL_CHESS_CNT, CHESSBOARD_HEIGHT


class Chessman(object):

    def to_dict(self):
        return {
            'id': self.id,
            'is_alive': self.is_alive,
            'position': self.position.to_dict()
        }

    @staticmethod
    def from_dict(data):
        chessman = Chessman(data['id'])
        chessman._current_position = GlobalPosition.from_dict(data['position'])
        chessman._is_alive = data['is_alive']
        return chessman

    def __init__(self, chess_id):
        if chess_id < 0 or chess_id >= TOTAL_CHESS_CNT:
            raise ValueError("Invalid chess id {}".format(chess_id))
        self._chess_id = chess_id
        self._color = Chessman._id2color(chess_id)
        self._role = Chessman._id2role(chess_id)
        self._init_global_position = Chessman._calc_init_position(chess_id)
        self._current_position = Chessman._calc_init_position(chess_id)
        self._is_alive = True
        self._char = Chessman._role2char(self.role, self.color)

    def __str__(self):
        return self.char

    def __repr__(self):
        return '<{} {} {}>'.format(
            self.__class__.__qualname__, self.char, self.to_dict())

    @property
    def id(self):
        return self._chess_id

    @property
    def color(self):
        return self._color

    @property
    def role(self):
        return self._role

    @property
    def init_global_position(self):
        return self._init_global_position

    @property
    def position(self):
        return self._current_position

    @property
    def is_alive(self):
        return self._is_alive

    @property
    def char(self):
        return self._char

    @staticmethod
    def _calc_init_position(chess_id):
        MIRRORED_X = [3, 5, 2, 6, 1, 7, 0, 8, 1, 7, 0, 2, 4, 6, 8, 4]
        MIRRORED_Y = [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 3, 3, 3, 3, 3, 0]
        mirrored_id = chess_id % (TOTAL_CHESS_CNT // 2)
        init_x = MIRRORED_X[mirrored_id]
        if chess_id == mirrored_id:
            init_y = MIRRORED_Y[mirrored_id]
        else:
            init_y = CHESSBOARD_HEIGHT - 1 - MIRRORED_Y[mirrored_id]
        return GlobalPosition(init_x, init_y)

    @staticmethod
    def _id2color(chess_id):
        return (ChessColor.RED
                if chess_id < TOTAL_CHESS_CNT // 2
                else ChessColor.BLACK)

    @staticmethod
    def _id2role(chess_id):
        mirrored_id = chess_id % (TOTAL_CHESS_CNT // 2)
        if mirrored_id == 15:
            return ChessRole.SHUAI
        role_map = [
            ChessRole.SHI,
            ChessRole.XIANG,
            ChessRole.MA,
            ChessRole.JU,
            ChessRole.PAO,
            ChessRole.BING,
            ChessRole.BING,
            ChessRole.BING]
        return role_map[mirrored_id // 2]

    @staticmethod
    def _role2char(role, color=ChessColor.RED):
        charset = {
            ChessColor.RED: {
                ChessRole.SHI: "仕",
                ChessRole.XIANG: "相",
                ChessRole.MA: "傌",
                ChessRole.JU: "俥",
                ChessRole.PAO: "炮",
                ChessRole.BING: "兵",
                ChessRole.SHUAI: "帅"
            },
            ChessColor.BLACK: {
                ChessRole.SHI: "士",
                ChessRole.XIANG: "象",
                ChessRole.MA: "馬",
                ChessRole.JU: "車",
                ChessRole.PAO: "砲",
                ChessRole.BING: "卒",
                ChessRole.SHUAI: "将"
            }
        }
        return charset[color][role]
