__all__ = ["RedisAdapter"]


from utils import decode
from redis.asyncio import Redis
import makefun


class RedisAdapter:

    def __init__(self, original_client: Redis):
        self._client: Redis = original_client
        self.hset = self._client.hset
        self.expire = self._client.expire
        self.hdel = self._client.hdel
        self.delete = self._client.delete
        self.sadd = self._client.sadd
        self.srem = self._client.srem

    @decode
    @makefun.wraps(Redis.hgetall)
    async def hgetall(self, *args, **kwargs):
        async with self._client.pipeline(transaction=False) as pipe:
            pipe.hgetall(*args, **kwargs)
            return await pipe.execute()
