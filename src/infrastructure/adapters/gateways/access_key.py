__all__ = ["RedisAccessKeyCommandGateway", "RedisAccessKeyQueryGateway"]


from typing import Sequence, Any
from redis.asyncio import Redis

from domain import AccessKey, User, AccessKeyId

from application.ports.gateways.errors import GatewayFailedError
from application.ports import AccessKeyMapper
from application.exceptions import AccessKeyNotFound
from infrastructure.exceptions import create_error_aware_decorator
from infrastructure.models import AccessKey as DbAccessKey

network_error_aware = create_error_aware_decorator(
    {frozenset({ConnectionRefusedError, ConnectionResetError}): GatewayFailedError}
)
class RedisAccessKeyCommandGateway:

    def __init__(self, client: Redis, mapper: AccessKeyMapper):
        self._client: Redis = client
        self._mapper: AccessKeyMapper = mapper

    @network_error_aware("Cannot add access key: there is no place to add him")
    async def add(self, access_key: AccessKey) -> None:
        db_access_key: DbAccessKey = self._mapper.to_dto(access_key)
        await self._client.hset(
            db_access_key.id_,
            mapping=db_access_key.model_dump(exclude={"id_"}),
        )
        self._client.expire(
            db_access_key.id_,
            int((access_key.expire_at - access_key.created_at).total_seconds()),
        )

    async def delete(self, access_key: AccessKey) -> None:
        raise NotImplementedError


class RedisAccessKeyQueryGateway:
    
    def __init__(self, client: Redis, mapper: AccessKeyMapper):
        self._client: Redis = client
        self._mapper: AccessKeyMapper = mapper

    def _decode(self, raw_access_key: dict[bytes, bytes]) -> dict[str, Any]:
        return {k.decode(): v.decode() for k, v in raw_access_key.items()}
        
    @network_error_aware("Cannot find access key: access keys are lost. Try again later")
    async def by_id(self, access_key_id: AccessKeyId) -> AccessKey:
        serialized_data: dict[bytes, bytes] = await self._client.hgetall(access_key_id)

        if not serialized_data:
            raise AccessKeyNotFound("Access key with given id does not exists")
        
        return self._mapper.to_domain(DbAccessKey.model_validate(self._decode(serialized_data)))


    async def by_user(self, user: User) -> Sequence[AccessKey] | None:
        raise NotImplementedError
