from config import settings
from app.flask_ext import redis_client


class MatchDB(object):

    @staticmethod
    def _genkey(table, entry_id):
        return "{}-{}".format(table, entry_id)

    @staticmethod
    def set(table, entry_id, value, ex=settings.GAME_TTL,
            px=None, nx=False, xx=False):
        key = MatchDB._genkey(table, entry_id)
        return redis_client.set(key, value, ex, px, nx, xx)

    @staticmethod
    def get(table, entry_id):
        key = MatchDB._genkey(table, entry_id)
        redis_client.get(key)

    @staticmethod
    def dequeue(table, entry_id, block, timeout=settings.GAME_TTL):
        key = MatchDB._genkey(table, entry_id)
        if block:
            return redis_client.blpop(key, timeout=timeout)
        else:
            return redis_client.lpop(key)

    @staticmethod
    def enqueue(table, entry_id, value):
        key = MatchDB._genkey(table, entry_id)
        return redis_client.rpush(key, value)
