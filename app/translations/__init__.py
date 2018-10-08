import importlib

LANGUAGES = ["zh_CN", "zh_TW"]

_DICTS_CACHE = {}


def get_dicts():
    if not _DICTS_CACHE:
        for lang in LANGUAGES:
            lang_module = importlib.import_module(
                ".{}".format(lang), __package__)
            _DICTS_CACHE[lang] = lang_module.DICT
    return _DICTS_CACHE
