import datetime


def timestamp(fmt="%Y%m%d"):
    return datetime.datetime.utcnow().strftime(fmt)


def statics_version():
    return timestamp()[:-1] + '0'
