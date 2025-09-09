__all__ = ["RedisAccessKeyCommandGateway", "RedisAccessKeyQueryGateway"]


from typing import Sequence

from domain import AccessKey, User, AccessKeyId

from application.ports.gateways.errors import GatewayFailedError
from application.ports import AccessKeyMapper
from application.exceptions import AccessKeyNotFound
from infrastructure.exceptions import create_error_aware_decorator
from infrastructure.models import AccessKey as DbAccessKey
from ..redis_adapter import RedisAdapter as Redis

network_error_aware = create_error_aware_decorator(
    {frozenset({ConnectionRefusedError, ConnectionResetError}): GatewayFailedError}
)


# TODO: inject naming_convection for keys to remove repeating declaration
class RedisAccessKeyCommandGateway:

    def __init__(self, client: Redis, mapper: AccessKeyMapper):
        self._client: Redis = client
        self._mapper: AccessKeyMapper = mapper

    @network_error_aware("Cannot add access key: there is no place to add him")
    async def add(self, access_key: AccessKey) -> None:
        db_access_key: DbAccessKey = self._mapper.to_dto(access_key)

        user_index: str = f"user_access_keys:{db_access_key.user_id}"
        key_id: str = f"access_key:{db_access_key.id_}"

        ttl: int = int((access_key.expire_at - access_key.created_at).total_seconds())

        await self._client.hset(
            db_access_key.id_,
            mapping=db_access_key.model_dump(exclude={"id_"}),
        )
        await self._client.expire(
            db_access_key.id_,
            ttl,
        )
        await self._client.sadd(user_index, key_id)
        await self._client.expire(user_index, ttl)

    async def delete(self, access_key: AccessKey) -> None:
        db_access_key: DbAccessKey = self._mapper.to_dto(access_key)
        user_index: str = f"user_access_keys:{db_access_key.user_id}"
        key_id: str = f"access_key:{db_access_key.id_}"

        await self._client.delete(db_access_key.id_)
        await self._client.srem(user_index, key_id)


class RedisAccessKeyQueryGateway:

    def __init__(self, client: Redis, mapper: AccessKeyMapper):
        self._client: Redis = client
        self._mapper: AccessKeyMapper = mapper

    @network_error_aware(
        "Cannot find access key: access keys are lost. Try again later"
    )
    async def by_id(self, access_key_id: AccessKeyId) -> AccessKey:

        found_key: dict[str, str] | None = await self._client.hgetall(
            f"access_key:{access_key_id}"
        )

        if not found_key:
            raise AccessKeyNotFound("Access key with given id does not exists")

        return self._mapper.to_domain(
            DbAccessKey.model_validate({"id_": access_key_id, **found_key})
        )

    async def by_user(self, user: User) -> Sequence[AccessKey] | None:
        raise NotImplementedError
