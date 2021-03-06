from datetime import datetime

from flask import url_for
from flask import request

from app import translations
from .field_renderer import field_renderer
from config import settings


def timestamp(fmt="%Y%m%d"):
    return datetime.utcnow().strftime(fmt)


def _statics_version():
    return timestamp()[:-1] + '0'


def static_url_for(filename):
    return url_for('static',
                   filename=filename,
                   statics_version=_statics_version())


def gettext(string, *args):
    return LazyString(_translator, string, *args) if string else ""


def _translator(string, *args):
    locale = get_locale()
    dictionary = translations.get_dicts().get(locale, {})
    translated_string = dictionary.get(string, string)
    if args:
        return translated_string % args
    else:
        return translated_string


def get_locale():
    if request:
        loc = request.accept_languages.best_match(['zh_CN', 'zh_TW'])
        loc = loc or request.accept_languages.best_match(['zh'])
        loc = loc or request.accept_languages.best_match(['en'])
        return loc
    else:
        return None


class LazyString(str):
    def __new__(cls, func, string, *args):
        return str.__new__(cls)

    def __init__(self, func, string, *args):
        self.func = func
        self.string = string
        self.args = args

    def __repr__(self):
        if len(self.string) <= 30:
            string = self.string[:30]
        else:
            string = "{}...".format(self.string[:27])
        return "<{}, {}>".format(self.__class__.__name__, string)

    def __str__(self):
        return self.func(self.string, *self.args)


def render_field(field, *args, **kwargs):
    return field_renderer(field, *args, **kwargs)


def not_on_production(func):
    def wrapper(*args, **kwargs):
        if settings.ENV == 'prod':
            print("WARNING: do not call {} on production!".format(func))
            return None
        else:
            return func(*args, **kwargs)
    return wrapper
