import ast

from config import settings
from app.shared import utils
from app.flask_ext import redis_client


class MatchDB(object):

    @staticmethod
    def _genkey(table, entry_id):
        if entry_id is None:
            return table
        else:
            return "{}-{}".format(table, entry_id)

    @staticmethod
    def _str2strrepr(obj):
        if isinstance(obj, str):
            return '"""{}"""'.format(obj)
        return obj

    @staticmethod
    def _repr2obj(obj):
        if obj is None:
            return None
        if isinstance(obj, str):
            return ast.literal_eval(obj)
        if isinstance(obj, list):
            return [MatchDB._repr2obj(item) for item in obj]
        return obj

    @staticmethod
    def set(table, entry_id, value, ex=settings.GAME_TTL,
            px=None, nx=False, xx=False):
        key = MatchDB._genkey(table, entry_id)
        value = MatchDB._str2strrepr(value)
        return redis_client.set(key, value, ex, px, nx, xx)

    @staticmethod
    def get(table, entry_id, ex=settings.GAME_TTL):
        key = MatchDB._genkey(table, entry_id)
        result = redis_client.get(key)
        redis_client.expire(key, ex)
        return MatchDB._repr2obj(result)

    @staticmethod
    def delete(table, entry_id, ex=settings.GAME_TTL):
        key = MatchDB._genkey(table, entry_id)
        result = redis_client.delete(key)
        # redis_client.expire(key, ex)
        return result

    @staticmethod
    def dequeue(table, entry_id, block, timeout=settings.GAME_TTL,
                ex=settings.GAME_TTL):
        key = MatchDB._genkey(table, entry_id)
        if block:
            result = redis_client.blpop(key, timeout=timeout)
            if result is not None:
                result = result[1]
        else:
            result = redis_client.lpop(key)
        redis_client.expire(key, ex)
        return MatchDB._repr2obj(result)

    @staticmethod
    def enqueue(table, entry_id, value, ex=settings.GAME_TTL):
        key = MatchDB._genkey(table, entry_id)
        value = MatchDB._str2strrepr(value)
        result = redis_client.rpush(key, value)
        redis_client.expire(key, ex)
        return result

    @staticmethod
    def force_remove_from_queue(table, entry_id, value, ex=settings.GAME_TTL):
        key = MatchDB._genkey(table, entry_id)
        result = redis_client.lrem(key, 0, value)
        redis_client.expire(key, ex)
        return MatchDB._repr2obj(result)

    @staticmethod
    def get_queue(table, entry_id, ex=settings.GAME_TTL):
        key = MatchDB._genkey(table, entry_id)
        result = redis_client.lrange(key, 0, -1)
        redis_client.expire(key, ex)
        return MatchDB._repr2obj(result)

    @staticmethod
    def takeaway(table, entry_id, ex=settings.GAME_TTL):
        key = MatchDB._genkey(table, entry_id)
        pipe = redis_client.pipeline(transaction=True)
        results = pipe.get(key).delete(key).execute()
        return MatchDB._repr2obj(results[0])

    @staticmethod
    @utils.not_on_production
    def dump_table(table):
        keys = redis_client.keys('{}*'.format(table))
        return MatchDB._repr2obj(redis_client.mget(keys))

    @staticmethod
    def lock(table, entry_id, blocking_timeout=0):
        key = MatchDB._genkey('lock-{}'.format(table), entry_id)
        redis_lock = redis_client.lock(
            key, timeout=settings.GAME_TTL, blocking_timeout=settings.GAME_TTL)
        return redis_lock, redis_lock.acquire(
            key, blocking_timeout=blocking_timeout)

    @staticmethod
    def enter_private_match(join_token):
        key = MatchDB._genkey('private_match_population', join_token)
        population = redis_client.incr(key)
        redis_client.expire(key, settings.GAME_TTL)
        if population > 2:
            redis_client.decr(key)
        return population

    @staticmethod
    def leave_private_match(join_token):
        key = MatchDB._genkey('private_match_population', join_token)
        population = redis_client.decr(key)
        redis_client.expire(key, settings.GAME_TTL)
        assert(population >= 0)
