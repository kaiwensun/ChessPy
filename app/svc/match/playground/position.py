from app.svc.match.playground.consts import CHESSBOARD_HEIGHT, CHESSBOARD_WIDTH


class GlobalPosition(object):
    """
    Global position of chessman. In red player's view, bottom-left is (0, 0), a
    red JU. The chess board's indexing is also using this rule. The position
    should never be out of the chess board.
    """

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._validate()

    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y
        }

    @staticmethod
    def from_dict(data):
        return GlobalPosition(data['x'], data['y'])

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self._validate()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        self._validate()

    def _validate(self):
        if self.x < 0 or self.x > CHESSBOARD_WIDTH - 1 \
                or self.y < 0 or self.y > CHESSBOARD_HEIGHT - 1:
            raise ValueError(
                'Illegal global position {}'.format(self.__str__()))

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__qualname__, self.to_dict())
