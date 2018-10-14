import hashlib
import hmac
import uuid

import flask_login

from app.shared import utils
from app.svc.membership.models import User
from app.flask_ext import login_manager, db

_USER_DATABASE = {}
_TIME_FORMAT_ = '%Y%m%d%H%M%S%f'
_ALT_ID_SPLITER_ = '-'


class SignedInUser(flask_login.UserMixin):
    def __init__(self, user_dict):
        super().__init__()
        self._alternative_id = "{}{}{}".format(
            user_dict['user_id'],
            _ALT_ID_SPLITER_,
            user_dict['pw_created_at'])
        self._dict = user_dict.copy()
        del self._dict['hashed_pw']
        keys = list(self._dict.keys())
        for k in keys:
            if k.startswith('_') or k == 'metadata':
                self._dict.pop(k)
        for k, v in self._dict.items():
            setattr(self, k, v)

    def get_id(self):
        return self._alternative_id

    # for testing only. will be removed.
    def _to_dict(self):
        return self._dict.copy()


def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return SignedInUser(user.__dict__)
    return None


def get_user_by_email(email):
    user = User.query.filter_by(email=email).one_or_none()
    if user:
        return SignedInUser(user.__dict__)
    return None


def create_user(name, email, password):
    if User.query.filter_by(email=email).first():
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
    db_user = User(**user)
    db.session.add(db_user)
    db.session.commit()
    return SignedInUser(user)


def uuid_len():
    return 32


@login_manager.user_loader
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
    user = User.query.get(user_id)
    expected = user and user.hashed_pw
    hashed = _hash(password)
    if expected is None:
        hmac.compare_digest(hashed, hashed)
        return False
    else:
        return hmac.compare_digest(hashed, expected)


def _hash(string):
    return hashlib.sha3_256(string.encode("utf")).hexdigest()


def get_all_users(limit=100):
    limit = max(0, limit)
    users = User.query.limit(limit).all()
    limit = min(limit, len(users))
    return [SignedInUser(user.__dict__) for user in users]
