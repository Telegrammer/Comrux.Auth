__all__ = ["RedisAccessKeyMapper"]


from datetime import datetime


from domain import AccessKey, AccessKeyId, UserId
from domain.value_objects import PassedDatetime, FutureDatetime
from functools import singledispatchmethod


from application.ports.mappers import AccessKeyMapper, MappingError
from infrastructure.models import AccessKeyDto
from infrastructure.exceptions import create_error_aware_decorator
from pydantic import ValidationError

type_mismatch_aware = create_error_aware_decorator(
    {frozenset({TypeError, AttributeError, ValidationError}): MappingError}
)


# TODO: resolve nest problem with create_error_aware_decorator
class RedisAccessKeyMapper(AccessKeyMapper[AccessKeyDto]):

    def to_string(self, id_: AccessKeyId) -> str:
        return f"access_key:{id_}"

    def to_dto(self, entity: AccessKey) -> AccessKeyDto:
        try:
            return AccessKeyDto(
                id_=entity.id_,
                user_id=entity.user_id,
                created_at=entity.created_at.isoformat(),
                expire_at=entity.expire_at.isoformat(),
            )
        except (TypeError, AttributeError, ValidationError, ValueError):
            raise MappingError("Cannot complete operation")

    @singledispatchmethod
    def to_domain(self, dto) -> AccessKey:
        raise MappingError(f"Unsupported dto type: {type(dto)}")

    @to_domain.register
    def _(self, dto: AccessKeyDto) -> AccessKey:
        try:
            issued_at: datetime = datetime.fromisoformat(dto.created_at)
            expire_at: datetime = datetime.fromisoformat(dto.expire_at)
            return AccessKey(
                id_=AccessKeyId(dto.id_),
                user_id=UserId(dto.user_id),
                created_at=PassedDatetime(issued_at, issued_at),
                expire_at=FutureDatetime(expire_at, issued_at),
            )
        except (TypeError, AttributeError, ValidationError, ValueError):
            raise MappingError("Cannot complete operation")

    @to_domain.register
    def _(self, dto: dict) -> AccessKey:
        return self.to_domain(AccessKeyDto.model_validate(dto))
