import hashlib
import hmac
import datetime

_USER_DATABASE = {}
_USER_INCREMENTER = len(_USER_DATABASE)


def get_user(id):
    user = _USER_DATABASE.get(id)
    del user['hashed_pw']
    return user


def create_user(name, email, password):
    global _USER_INCREMENTER
    for user in _USER_DATABASE.values():
        if user['email'] == email:
            return None
    user = {
        'id': str(_USER_INCREMENTER),
        'name': name,
        'email': email,
        'hashed_pw': _hash(password)
    }
    _USER_DATABASE[str(_USER_INCREMENTER)] = user
    _USER_INCREMENTER += 1
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
create_user('Kaiwen Sun', 'kaiwen@fake_data.com', 'password1')
