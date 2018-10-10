import sys
_NOT_SET_ = "_NOT_SET_"

# These settings can be overridden by local_settings.py
DEV_PORT_NUMBER = 8888
DEBUG_MODE = True
ENV = _NOT_SET_
FLASK_APP_SECRET_KEY = _NOT_SET_


thismodule = sys.modules[__name__]
try:
    import local_settings
    for key in dir(local_settings):
        setattr(thismodule, key, getattr(local_settings, key))
except ModuleNotFoundError:
    pass

for key in dir(thismodule):
    if key is not "_NOT_SET_" and getattr(thismodule, key) is _NOT_SET_:
        raise Exception("%s should be set in local_settings." % key)
