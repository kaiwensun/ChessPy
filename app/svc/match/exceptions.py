class BaseMatchException(Exception):
    pass


class CannotCreateMatchException(BaseMatchException):
    pass


class CannotJoinMatchException(BaseMatchException):
    pass


class AlreadyInMatchException(BaseMatchException):
    pass


class FullRoomException(BaseMatchException):
    pass
