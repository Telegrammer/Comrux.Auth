__all__ = ["RedisEmailVerificationMapper"]


from datetime import datetime
from pydantic import ValidationError

from domain import EmailVerification, UserId
from domain.value_objects import FutureDatetime, Uuid7, TokenHash
from functools import singledispatchmethod

from application.ports import EmailVerififcationMapper
from application.ports.mappers.errors import MappingError

from infrastructure.exceptions import create_error_aware_decorator
from infrastructure.models import EmailVerificationDto

type_mismatch_aware = create_error_aware_decorator(
    {frozenset({TypeError, AttributeError, ValidationError}): MappingError}
)


class RedisEmailVerificationMapper(EmailVerififcationMapper[EmailVerificationDto]):

    @type_mismatch_aware("Inner models structure mismatch appeared")
    def to_dto(self, entity: EmailVerification) -> EmailVerificationDto:
        return EmailVerificationDto(
            id_=entity.id_,
            user_id=entity.user_id,
            token_hash=entity.token_hash,
            expire_at=entity.expire_at.isoformat(),
            used=int(entity.used),
            used_at=entity.used_at.isoformat() if entity.used_at else "",
        )

    @singledispatchmethod
    def to_domain(self, dto) -> EmailVerification:
        raise MappingError(f"Unsupported dto type: {type(dto)}")

    @to_domain.register
    @type_mismatch_aware("Inner models structure mismatch appeared")
    def _(self, dto: EmailVerificationDto) -> EmailVerification:
        expire_at: datetime = datetime.fromisoformat(dto.expire_at)
        used_at: datetime = datetime.fromisoformat(dto.used_at)
        id_: Uuid7 = Uuid7(dto.id_)
        return EmailVerification(
            id_=id_,
            user_id=UserId(dto.user_id),
            token_hash=TokenHash(dto.token_hash),
            expire_at=FutureDatetime(expire_at, id_.issued_at),
            used=dto.used,
            used_at=used_at,
        )

    @to_domain.register
    @type_mismatch_aware("Inner models structure mismatch appeared")
    def _(self, dto: dict) -> EmailVerification:
        return self.to_domain(EmailVerificationDto.model_validate(dto))
