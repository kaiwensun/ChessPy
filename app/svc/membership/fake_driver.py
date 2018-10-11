import hashlib
import hmac
import uuid

import flask_login

from app.shared import utils

_USER_DATABASE = {}
_TIME_FORMAT_ = '%Y%m%d%H%M%S%f'
_ALT_ID_SPLITER_ = '-'


class User(flask_login.UserMixin):
    def __init__(self, user_dict):
        super().__init__()
        self._alternative_id = "{}{}{}".format(
            user_dict['user_id'],
            _ALT_ID_SPLITER_,
            user_dict['pw_created_at'])
        self._dict = user_dict.copy()
        del self._dict['hashed_pw']
        for k, v in self._dict.items():
            setattr(self, k, v)

    def get_id(self):
        return self._alternative_id

    # for testing only. will be removed.
    def _to_dict(self):
        return self._dict.copy()


def get_user(user_id):
    user = _USER_DATABASE.get(user_id)
    if user:
        return User(user)
    return None


def get_user_by_email(email):
    users = filter(
        lambda user: user['email'] == email,
        _USER_DATABASE.values())
    for user in users:
        return User(user)
    return None


def create_user(name, email, password):
    for user in _USER_DATABASE.values():
        if user['email'] == email:
            return None
    now = utils.timestamp(_TIME_FORMAT_)
    user = {
        'user_id': uuid.uuid4().hex,
        'name': name,
        'email': email,
        'hashed_pw': _hash(password),
        'pw_created_at': now,
        'created_at': now
    }
    _USER_DATABASE[user['user_id']] = user
    return User(user)


def uuid_len():
    return 32


def get_user_by_alternative_id(alternative_id):
    if not alternative_id or len(alternative_id) != 32 + 1 + 20:
        return None
    user_id = alternative_id[:uuid_len()]
    user = get_user(user_id)
    if user and user.get_id() == alternative_id:
        return user
    return None


def verify_user(user_id, password):
    # Some tedious work to prevent timing analysis
    expected = _USER_DATABASE.get(user_id, {}).get('hashed_pw')
    hashed = _hash(password)
    if expected is None:
        hmac.compare_digest(hashed, hashed)
        return False
    else:
        return hmac.compare_digest(hashed, expected)


def _hash(string):
    return hashlib.sha3_256(string.encode("utf")).hexdigest()


# Create an existing user
create_user('Kaiwen Sun', 'kaiwen@fakedata.com', 'password1')
