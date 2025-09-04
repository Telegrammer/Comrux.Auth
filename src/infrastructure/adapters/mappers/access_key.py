__all__ = ["RedisAccessKeyMapper"]


from datetime import datetime


from domain import AccessKey, AccessKeyId, UserId
from domain.value_objects import PassedDatetime, FutureDatetime


from application.ports.mappers import AccessKeyMapper, MappingError
from infrastructure.models import AccessKey as DbAccessKey
from infrastructure.exceptions import create_error_aware_decorator


type_mismatch_aware = create_error_aware_decorator({
    frozenset({TypeError, AttributeError}): MappingError
})

class RedisAccessKeyMapper(AccessKeyMapper[DbAccessKey]):


    @type_mismatch_aware
    def to_dto(self, entity: AccessKey) -> DbAccessKey:
        return DbAccessKey(
            id_=f"access_key:{entity.id_}",
            user_id=entity.user_id,
            created_at=entity.created_at.isoformat(),
            expire_at=entity.expire_at.isoformat(),
        )

    @type_mismatch_aware
    def to_domain(self, dto: DbAccessKey) -> AccessKey:
        issued_at: datetime = datetime.fromisoformat(dto.created_at)
        expire_at: datetime = datetime.fromisoformat(dto.expire_at)
        return AccessKey(
            id_=AccessKeyId(dto.id_),
            user_id=UserId(dto.user_id),
            created_at=PassedDatetime(issued_at, issued_at),
            expire_at=FutureDatetime(expire_at, issued_at),
        )
