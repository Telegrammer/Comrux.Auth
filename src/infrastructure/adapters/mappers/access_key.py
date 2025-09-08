__all__ = ["RedisAccessKeyMapper"]


from datetime import datetime


from domain import AccessKey, AccessKeyId, UserId
from domain.value_objects import PassedDatetime, FutureDatetime
from functools import singledispatchmethod


from application.ports.mappers import AccessKeyMapper, MappingError
from infrastructure.models import AccessKey as DbAccessKey
from infrastructure.exceptions import create_error_aware_decorator
from pydantic import ValidationError

type_mismatch_aware = create_error_aware_decorator(
    {frozenset({TypeError, AttributeError, ValidationError}): MappingError}
)


class RedisAccessKeyMapper(AccessKeyMapper[DbAccessKey]):

    def to_dto(self, entity: AccessKey) -> DbAccessKey:
        try:
            return DbAccessKey(
                id_=f"access_key:{entity.id_}",
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
    def _(self, dto: DbAccessKey) -> AccessKey:
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
        return self.to_domain(DbAccessKey.model_validate(dto))
