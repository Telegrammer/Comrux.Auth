__all__ = ["RedisAccessKeyCommandGateway", "RedisAccessKeyQueryGateway"]


from typing import Sequence
import makefun

from domain import AccessKey, User, AccessKeyId, UserId

from application.ports.gateways.errors import GatewayFailedError
from application.ports import AccessKeyMapper
from application.exceptions import AccessKeyNotFound
from infrastructure.exceptions import create_error_aware_decorator
from infrastructure.models import AccessKeyDto
from ..redis_adapter import RedisAdapter as Redis

network_error_aware = create_error_aware_decorator(
    {frozenset({ConnectionRefusedError, ConnectionResetError}): GatewayFailedError}
)

class DbUserIndex:

    def __init__(self, user_id: UserId):
        self._user_id = user_id
    
    def __str__(self):
        return f"user_access_keys:{self._user_id}"
class DbAccessKey:

    def __init__(self, key: AccessKeyDto):
        self._key = key

    @property
    def id_(self) -> str:
        return f"access_key:{self._key.id_}"

    @property
    def user_index(self) -> str:
        return str(DbUserIndex(self._key.user_id))

    def as_dict(self) -> dict[str, str]:
        return {
            "user_id": self._key.user_id,
            "created_at": self._key.created_at,
            "expire_at": self._key.expire_at,
        }

    @staticmethod
    def create(obj: dict[str, str]) -> AccessKeyDto:
        return AccessKeyDto.model_validate(obj)

    @staticmethod
    def create_id(access_key_id: AccessKeyId) -> str:
        return f"access_key:{access_key_id}"


class RedisAccessKeyCommandGateway:

    def __init__(self, client: Redis, mapper: AccessKeyMapper):
        self._client: Redis = client
        self._mapper: AccessKeyMapper = mapper

    @network_error_aware("Cannot add access key: there is no place to add him")
    async def add(self, access_key: AccessKey) -> None:
        db_access_key: DbAccessKey = DbAccessKey(self._mapper.to_dto(access_key))

        ttl: int = int((access_key.expire_at - access_key.created_at).total_seconds())

        await self._client.hset(
            db_access_key.id_,
            mapping=db_access_key.as_dict(),
        )
        await self._client.expire(
            db_access_key.id_,
            ttl,
        )
        await self._client.sadd(db_access_key.user_index, db_access_key.id_)
        await self._client.expire(db_access_key.user_index, ttl)

    @network_error_aware("Cannot delete access key: can't reach to him")
    async def delete(self, access_key: AccessKey) -> None:
        db_access_key: DbAccessKey = DbAccessKey(self._mapper.to_dto(access_key))
        await self._client.delete(db_access_key.id_)
        await self._client.srem(db_access_key.user_index, db_access_key.id_)

    @network_error_aware("Cannot delete access keys: can't reach to them")
    async def delete_keys_by_user_id(self, user_id: UserId) -> None:
        user_index: str = str(DbUserIndex(user_id))
        keys = await self._client.smembers(user_index)
        if keys:
            await self._client.delete(*keys)
        await self._client.delete(user_index)



class RedisAccessKeyQueryGateway:

    def __init__(self, client: Redis, mapper: AccessKeyMapper):
        self._client: Redis = client
        self._mapper: AccessKeyMapper = mapper

    @network_error_aware(
        "Cannot find access key: access keys are lost. Try again later"
    )
    async def by_id(self, access_key_id: AccessKeyId) -> AccessKey:

        found_key: dict[str, str] | None = await self._client.hgetall(
            DbAccessKey.create_id(access_key_id)
        )

        if not found_key:
            raise AccessKeyNotFound("Access key with given id does not exists")

        return self._mapper.to_domain(
            DbAccessKey.create({"id_": access_key_id, **found_key})
        )

    async def by_user(self, user: User) -> Sequence[AccessKey] | None:
        raise NotImplementedError
