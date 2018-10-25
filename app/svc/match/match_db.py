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
    def set(table, entry_id, value, ex=settings.GAME_TTL,
            px=None, nx=False, xx=False):
        key = MatchDB._genkey(table, entry_id)
        return redis_client.set(key, value, ex, px, nx, xx)

    @staticmethod
    def get(table, entry_id, ex=settings.GAME_TTL):
        key = MatchDB._genkey(table, entry_id)
        result = redis_client.get(key)
        redis_client.expire(key, ex)
        return result

    @staticmethod
    def delete(table, entry_id, ex=settings.GAME_TTL):
        key = MatchDB._genkey(table, entry_id)
        result = redis_client.delete(key)
        redis_client.expire(key, ex)
        return result

    @staticmethod
    def dequeue(table, entry_id, block, timeout=settings.GAME_TTL,
                ex=settings.GAME_TTL):
        key = MatchDB._genkey(table, entry_id)
        if block:
            result = redis_client.blpop(key, timeout=timeout)
        else:
            result = redis_client.lpop(key)
        redis_client.expire(key, ex)
        return result

    @staticmethod
    def enqueue(table, entry_id, value, ex=settings.GAME_TTL):
        key = MatchDB._genkey(table, entry_id)
        result = redis_client.rpush(key, value)
        redis_client.expire(key, ex)
        return result

    @staticmethod
    def force_remove_from_queue(table, entry_id, value, ex=settings.GAME_TTL):
        key = MatchDB._genkey(table, entry_id)
        result = redis_client.lrem(key, 0, value)
        redis_client.expire(key, ex)
        return result

    @staticmethod
    def get_queue(table, entry_id, ex=settings.GAME_TTL):
        key = MatchDB._genkey(table, entry_id)
        result = redis_client.lrange(key, 0, -1)
        redis_client.expire(key, ex)
        return result

    @staticmethod
    def takeaway(table, entry_id, ex=settings.GAME_TTL):
        key = MatchDB._genkey(table, entry_id)
        pipe = redis_client.pipeline(transaction=True)
        results = pipe.get(key).delete(key).expire(key).execute()
        return results[0]

    @staticmethod
    @utils.not_on_production
    def dump_table(table):
        keys = redis_client.keys('{}*'.format(table))
        return redis_client.mget(keys)
