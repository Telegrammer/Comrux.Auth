from datetime import datetime

from domain.entities import UserId, AccessKey
from domain.ports import AccessKeyIdGenerator
from domain.value_objects import PassedDatetime, FutureDatetime
from domain.policies import AccessKeyValidityPolicy


class AccessKeyService:

    def __init__(
        self,
        id_generator: AccessKeyIdGenerator,
        validity_policy: AccessKeyValidityPolicy,
    ):
        self._id_generator: AccessKeyIdGenerator = id_generator
        self._validity_policy: AccessKeyValidityPolicy = validity_policy

    def create_access_key(self, user_id: UserId, now: datetime) -> AccessKey:

        return AccessKey(
            id_=self._id_generator(),
            user_id=user_id,
            created_at=PassedDatetime(now, now),
            expire_at=FutureDatetime(now + self._validity_policy.ttl, now),
        )

    def can_refresh(self, key: AccessKey, now: datetime) -> bool:
        ttl_total: int = (key.expire_at - key.created_at).total_seconds()
        ttl_left: int = (key.expire_at - now).total_seconds()
        return (
            ttl_total > 0
            and ttl_left >= self._validity_policy.min_freshness_precentage * ttl_total
        )
