import datetime
from flask import url_for

def timestamp(fmt="%Y%m%d"):
    return datetime.datetime.utcnow().strftime(fmt)


def _statics_version():
    return timestamp()[:-1] + '0'

def static_url_for(filename):
    return url_for('static',
                    filename=filename,
                    statics_version=_statics_version())
