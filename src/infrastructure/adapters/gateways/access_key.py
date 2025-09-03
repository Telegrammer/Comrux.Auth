__all__ = ["RedisAccessKeyCommandGateway", "RedisAccessKeyQueryGateway"]


from typing import Sequence
from redis.asyncio import Redis
from datetime import timedelta

from domain import AccessKey, User, AccessKeyId


class RedisAccessKeyCommandGateway:

    def __init__(self, client: Redis):
        self._client: Redis = client

    async def add(self, access_key: AccessKey) -> None:
        instance_name = f"access_key:{access_key.id_}"
        await self._client.hset(
            instance_name,
            mapping={
                "user_id": access_key.user_id,
                "created_at": access_key.created_at.isoformat(),
                "expire_at": access_key.expire_at.isoformat(),
            },
        )
        self._client.expire(
            instance_name,
            int((access_key.expire_at - access_key.created_at).total_seconds()),
        )

    async def delete(self, access_key: AccessKey) -> None:
        raise NotImplementedError


class RedisAccessKeyQueryGateway:

    async def by_id(self, access_key_id: AccessKeyId) -> AccessKey | None:
        raise NotImplementedError

    async def by_user(self, user: User) -> Sequence[AccessKey] | None:
        raise NotImplementedError
