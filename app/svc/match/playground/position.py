from app.svc.match.playground.consts import CHESSBOARD_HEIGHT, CHESSBOARD_WIDTH


class _BasePosition(object):
    """
    Global position of chessman. In red player's view, bottom-left is (0, 0), a
    red JU. The chess board's indexing is also using this rule. The position
    should never be out of the chess board.
    """

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._validate()

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
        pass

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __repr__(self):
        return '<{} ({}, {})>'.format(
            self.__class__.__qualname__, self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, tuple) and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        return isinstance(self, type(
            other)) and self.x == other.x and self.y == other.y

    def __neq__(self, other):
        return not self.__eq__(other)

    def to_tupple(self):
        return (self.x, self.y)


class GlobalPosition(_BasePosition):
    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y
        }

    @staticmethod
    def from_dict(data):
        return GlobalPosition(data['x'], data['y'])

    def _validate(self):
        if self.x < 0 or self.x > CHESSBOARD_WIDTH - 1 \
                or self.y < 0 or self.y > CHESSBOARD_HEIGHT - 1:
            raise ValueError(
                'Illegal global position {}'.format(self.__str__()))

    def __add__(self, delta):
        if isinstance(delta, PositionDelta):
            x, y = self.x + delta.x, self.y + delta.y
        elif isinstance(delta, tuple) and len(delta) == 2:
            x, y = self.x + delta[0], self.y + delta[1]
        else:
            raise TypeError(
                "param must be of type {} or length-2 tuple"
                .format(PositionDelta.__class__.__qualname__))
        return GlobalPosition(x, y)

    def __radd__(self, delta):
        return self + delta

    def __sub__(self, other):
        if isinstance(other, PositionDelta):
            return GlobalPosition(self.x - other.x, self.y - other.y)
        elif isinstance(other, GlobalPosition):
            return PositionDelta(self.x - other.x, self.y - other.y)
        elif isinstance(other, tuple) and len(tuple) == 2:
            # assume tuple is a delta. return a global position
            return GlobalPosition(self.x - other[0], self.y - other[1])
        else:
            raise TypeError(
                "param must be of type {} or {} or length-2 tuple".format(
                    GlobalPosition.__class__.__qualname__,
                    PositionDelta.__class__.__qualname__))

    def __rsub__(self, other):
        if isinstance(other, tuple) and len(tuple) == 2:
            return PositionDelta(other[0] - self.x, other[1] - self.y)
        else:
            raise TypeError("param must be of type length-2 tuple")

    def average_with(self, other):
        if isinstance(other, GlobalPosition):
            x, y = (self.x + other.x) // 2, (self.y + other.y) // 2
        elif isinstance(other, tuple) and len(other) == 2:
            x, y = (self.x + other[0]) // 2, (self.y + other[1]) // 2
        else:
            raise TypeError(
                "param must be of type {} or length-2 tuple".format(
                    GlobalPosition.__class__.__qualname__))
        return GlobalPosition(x, y)


class PositionDelta(_BasePosition):
    def _validate(self):
        if abs(self.x) > CHESSBOARD_WIDTH - 1 \
                or abs(self.y) > CHESSBOARD_HEIGHT - 1:
            raise ValueError(
                'Illegal global position {}'.format(self.__str__()))

    def __abs__(self):
        return PositionDelta(abs(self.x), abs(self.y))
