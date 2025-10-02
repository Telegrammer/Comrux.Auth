__all__ = ["RedisEmailVerificationCommandGateway", "RedisEmailVerificationQueryGateway"]


from typing import Sequence

from domain import EmailVerification
from domain.value_objects import Uuid7, TokenHash

from application.exceptions import EmailVerificationObjectNotFound
from application.ports.gateways.errors import GatewayFailedError
from application.ports import EmailVerififcationMapper
from infrastructure.exceptions import create_error_aware_decorator
from infrastructure.models import EmailVerificationDto
from ..redis_adapter import RedisAdapter as Redis

network_error_aware = create_error_aware_decorator(
    {frozenset({ConnectionRefusedError, ConnectionResetError}): GatewayFailedError}
)


class DbTokenHashIndex:

    def __init__(self, token_hash: TokenHash):
        self._hash = token_hash

    def __str__(self):
        return f"token_verification_objects:{self._hash}"


class DbEmailVerification:

    def __init__(self, verification_object: EmailVerificationDto):
        self._verfifcation_object = verification_object

    @property
    def id_(self) -> str:
        return f"email_verification:{self._verfifcation_object.id_}"

    @property
    def token_hash_index(self) -> str:
        return str(DbTokenHashIndex(self._verfifcation_object.token_hash))

    def as_dict(self) -> dict[str, str]:
        return {
            "id_": self._verfifcation_object.id_,
            "user_id": self._verfifcation_object.user_id,
            "token_hash": self._verfifcation_object.token_hash,
            "expire_at": self._verfifcation_object.expire_at,
            "used": self._verfifcation_object.used,
            "used_at": self._verfifcation_object.used_at,
        }

    @staticmethod
    def create(obj: dict[str, str]) -> EmailVerificationDto:
        return EmailVerificationDto.model_validate(obj)

    @staticmethod
    def create_id(email_verification_id: Uuid7) -> str:
        return f"email_verification:{email_verification_id}"


class RedisEmailVerificationCommandGateway:

    def __init__(self, client: Redis, mapper: EmailVerififcationMapper):
        self._client: Redis = client
        self._mapper: EmailVerififcationMapper = mapper

    @network_error_aware("Cannot add access key: there is no place to add him")
    async def add(self, verification_object: EmailVerification) -> None:
        db_verification_obj: DbEmailVerification = DbEmailVerification(self._mapper.to_dto(verification_object))

        ttl: int = int(
            (
                verification_object.expire_at
                - getattr(verification_object, "__object_id_").issued_at
            ).total_seconds()
        )

        await self._client.hset(
            db_verification_obj.id_,
            mapping=db_verification_obj.as_dict(),
        )
        await self._client.expire(
            db_verification_obj.id_,
            ttl,
        )
        await self._client.sadd(db_verification_obj.token_hash_index, db_verification_obj.id_)
        await self._client.expire(db_verification_obj.token_hash_index, ttl)

    #TODO: add delete method to email verification objects

class RedisEmailVerificationQueryGateway:

    def __init__(self, client: Redis, mapper: EmailVerififcationMapper):
        self._client: Redis = client
        self._mapper: EmailVerififcationMapper = mapper

    
    @network_error_aware(
        "Cannot find access key: access keys are lost. Try again later"
    )
    async def by_token_hash(self, token: TokenHash) -> Sequence[EmailVerification] | None:
        index = DbTokenHashIndex(token)
        ids: list[str] = await self._client.smembers(str(index))
        if not ids:
            raise EmailVerificationObjectNotFound

        results: list[EmailVerification] = []
        for id_ in ids:
            data: dict[str, str] = await self._client.hgetall(id_)
            if not data:
                continue
            dto = DbEmailVerification.create(data)
            results.append(self._mapper.to_domain(dto))

        return results or None
        

