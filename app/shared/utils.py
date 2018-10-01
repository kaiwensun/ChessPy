import datetime


def timestamp(fmt="%%Y%%m%%d"):
    return datetime.datetime.utcnow().strftime(fmt)
