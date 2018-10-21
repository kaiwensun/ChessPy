class BaseMatchException(Exception):
    pass


class AlreadyInMatchException(BaseMatchException):
    pass


class NoMatchFoundException(BaseMatchException):
    pass
