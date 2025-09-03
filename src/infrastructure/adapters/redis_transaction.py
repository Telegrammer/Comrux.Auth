__all__ = ["RedisTransaction"]


from redis.asyncio import Redis


from application.ports import Transaction


class RedisTransaction(Transaction):

    def __init__(self, client: Redis):
        self._client: Redis = client
    
    async def complete(self):
        await self._client.execute()

    async def cancel(self):
        await self._client.reset()