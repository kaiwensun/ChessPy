import hashlib
import hmac
import datetime
import uuid

_USER_DATABASE = {}


def get_user(id):
    user = _USER_DATABASE.get(id)
    if user:
        user_copy = user.copy()
        del user_copy['hashed_pw']
        return user_copy
    return None


def get_user_by_email(email):
    users = filter(
        lambda user: user['email'] == email,
        _USER_DATABASE.values())
    for user in users:
        user_copy = user.copy()
        del user_copy['hashed_pw']
        return user_copy
    return None


def create_user(name, email, password):
    for user in _USER_DATABASE.values():
        if user['email'] == email:
            return None
    user = {
        'id': uuid.uuid4().hex,
        'name': name,
        'email': email,
        'hashed_pw': _hash(password)
    }
    _USER_DATABASE[user['id']] = user
    return user


def verify_user(id, password):
    # Some tedious work to prevent timing analysis
    expected = _USER_DATABASE.get(id, {}).get('hashed_pw')
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
