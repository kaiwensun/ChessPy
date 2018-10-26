class BaseMatchException(Exception):
    pass


class AlreadyInMatchException(BaseMatchException):
    pass


class NoMatchFoundException(BaseMatchException):
    pass


class InvalidMatchState(BaseMatchException):
    pass


class CannotAcquireMatchDoor(BaseMatchException):
    pass
