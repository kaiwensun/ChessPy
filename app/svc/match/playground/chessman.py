from app.svc.match.playground.chess_color import ChessColor
from app.svc.match.playground.chess_role import ChessRole
from app.svc.match.playground.position import GlobalPosition
from app.svc.match.playground.consts import TOTAL_CHESS_CNT, CHESSBOARD_HEIGHT


class Chessman(object):

    def to_dict(self):
        return {
            'id': self.id,
            'position': self.position.to_dict()
        }

    @staticmethod
    def from_dict(data):
        chessman = Chessman(data['id'])
        chessman._current_position = GlobalPosition.from_dict(data['position'])
        return chessman

    def __init__(self, chess_id):
        if chess_id < 0 or chess_id >= TOTAL_CHESS_CNT:
            raise ValueError("Invalid chess id {}".format(chess_id))
        self._chess_id = chess_id
        self._color = Chessman.id2color(chess_id)
        self._role = Chessman.id2role(chess_id)
        self._init_global_position = Chessman._calc_init_position(chess_id)
        self._current_position = Chessman._calc_init_position(chess_id)

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

    @position.setter
    def position(self, position):
        if not (isinstance(position, GlobalPosition) or (position is None)):
            raise TypeError(
                "chessman position must be of type {}".format(
                    GlobalPosition.__class__.__qualname__))
        self._current_position = position

    @property
    def char(self):
        return Chessman.role2char(self.role, self.color)

    @property
    def pic(self):
        return Chessman.role2pic(self.role, self.color)

    def can_exist_at(self, position):
        if not isinstance(position, GlobalPosition):
            raise TypeError(
                "expecting {}".format(
                    GlobalPosition.__class__.__qualname__))
        px = position.x
        py = position.y
        if self.color == ChessColor.BLACK:
            py = CHESSBOARD_HEIGHT - 1 - py
        if self.role is ChessRole.SHI:
            if py in [0, 2]:
                return px in [3, 5]
            elif py == 1:
                return px == 4
        elif self.role is ChessRole.XIANG:
            if py in [0, 4]:
                return px in [2, 6]
            elif py == 2:
                return px == 4
        elif self.role in [ChessRole.MA, ChessRole.JU, ChessRole.PAO]:
            return True
        elif self.role is ChessRole.BING:
            if py > 4:
                return True
            elif py in [3, 4]:
                return px in [0, 2, 4, 6, 8]
        elif self.role is ChessRole.SHUAI:
            return (3 <= px and px <= 5) and (
                (0 <= py and py <= 2) or (py <= 7 and py <= 9))
        return False

    def can_reach(self, position, chessboard):

        def can_reach_straight(delta, expect_blocker_cnt):
            if delta.x != 0 and delta.y != 0:
                return False
            blocker = GlobalPosition(self.position.x, self.position.y)
            for attr_i, attr_j in [('x', 'y'), ('y', 'x')]:
                if getattr(delta, attr_i) == 0:
                    delta_step = 1 if getattr(delta, attr_j) > 0 else -1
                    for _ in range(getattr(abs(delta), attr_j) - 1):
                        new_step = getattr(blocker, attr_j) + delta_step
                        setattr(blocker, attr_j, new_step)
                        if chessboard.get_chessman(blocker):
                            expect_blocker_cnt -= 1
                            if expect_blocker_cnt < 0:
                                return False
            return expect_blocker_cnt == 0

        if not isinstance(position, GlobalPosition):
            raise TypeError(
                "expecting {}".format(
                    GlobalPosition.__class__.__qualname__))
        dst_chessman = chessboard.get_chessman(position)
        if dst_chessman and dst_chessman.color == self.color:
            return False
        if self.position == position:
            return False
        delta = position - self.position
        if self.role is ChessRole.SHI:
            return abs(delta) == (1, 1)
        elif self.role is ChessRole.XIANG:
            if abs(delta) != (2, 2):
                return False
            blocker = self.position.average_with(position)
            if chessboard.get_chessman(blocker):
                return False
            return True
        elif self.role is ChessRole.MA:
            absdelta = abs(delta)
            if absdelta != (1, 2) and absdelta != (2, 1):
                return False
            blocker = self.position.average_with(position)
            if absdelta.x == 2:
                blocker.y = self.position.y
            else:
                blocker.x = self.position.x
            if chessboard.get_chessman(blocker):
                return False
            return True
        elif self.role is ChessRole.JU:
            return can_reach_straight(delta, 0)
        elif self.role is ChessRole.PAO:
            target = chessboard.get_chessman(position)
            if target:
                return can_reach_straight(delta, 1)
            else:
                return can_reach_straight(delta, 0)
        elif self.role is ChessRole.BING:
            if abs(delta.x) + abs(delta.y) != 1:
                return False
            if self.color == ChessColor.RED:
                return delta.y >= 0
            else:
                return delta.y <= 0
        elif self.role is ChessRole.SHUAI:
            absdelta = abs(delta)
            if absdelta.x + absdelta.y == 1:
                return True
            if (dst_chessman.color != self.color
                    and dst_chessman.role == self.role):
                return True
            return False
        else:
            raise ValueError(self.role)

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
    def id2color(chess_id):
        return (ChessColor.RED
                if chess_id < TOTAL_CHESS_CNT // 2
                else ChessColor.BLACK)

    @staticmethod
    def id2role(chess_id):
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
    def role2char(role, color=ChessColor.RED):
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

    @staticmethod
    def role2pic(role, color=ChessColor.RED):
        charset = {
            ChessColor.RED: {
                ChessRole.SHI: "q",
                ChessRole.XIANG: "b",
                ChessRole.MA: "h",
                ChessRole.JU: "r",
                ChessRole.PAO: "f",
                ChessRole.BING: "p",
                ChessRole.SHUAI: "k"
            },
            ChessColor.BLACK: {
                ChessRole.SHI: "w",
                ChessRole.XIANG: "n",
                ChessRole.MA: "j",
                ChessRole.JU: "t",
                ChessRole.PAO: "|",
                ChessRole.BING: "o",
                ChessRole.SHUAI: "l"
            }
        }
        return charset[color][role]
