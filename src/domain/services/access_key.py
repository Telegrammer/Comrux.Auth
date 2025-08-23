from datetime import datetime, timedelta

from domain.entities import UserId, AccessKey
from domain.ports import AccessKeyIdGenerator
from domain.value_objects import FutureDatetime, PassedDatetime


class AccessKeyService:

    def __init__(self, id_generator: AccessKeyIdGenerator, expiration_time: timedelta):
        self._id_generator = id_generator
        self._expiration_time: timedelta = expiration_time

    def create_access_key(self, user_id: UserId, now: datetime) -> AccessKey:

        return AccessKey(
            id_=self._id_generator(),
            user_id=user_id,
            created_at=PassedDatetime(now, now),
            expire_at=FutureDatetime(now + self._expiration_time, now),
        )

    def is_expired(self, access_key: AccessKey, now: datetime) -> bool:
        return now >= access_key.expire_at
