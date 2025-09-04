__all__ = ["StatelessRefreshRequest", "StatelessRefreshUsecase"]

from datetime import datetime
from dataclasses import dataclass

from domain import AccessKeyId, AccessKey, UserId, AccessKeyService
from domain.value_objects import PassedDatetime, FutureDatetime

from .contract import RefreshRequest, RefreshResponse

from application.ports import Clock
from application.exceptions import ExpiredAccessKeyError


@dataclass(slots=True, kw_only=True, frozen=True)
class StatelessRefreshRequest(RefreshRequest):

    user_id: UserId
    created_at: PassedDatetime
    expire_at: FutureDatetime

    @classmethod
    def from_primitives(
        cls, *, key_id: str, user_id: str, created_at: datetime, expire_at: datetime
    ) -> "StatelessRefreshRequest":

        return cls(
            access_key_id=AccessKeyId(key_id),
            user_id=UserId(user_id),
            created_at=PassedDatetime(created_at, created_at),
            expire_at=FutureDatetime(expire_at, created_at),
        )


class StatelessRefreshUsecase:

    def __init__(
        self,
        clock: Clock,
        access_key_service: AccessKeyService,
    ):
        self._clock: Clock = clock
        self._access_key_service: AccessKeyService = access_key_service

    async def __call__(self, request: StatelessRefreshRequest) -> RefreshResponse:

        now: datetime = self._clock.now()

        found_key: AccessKey = AccessKey(
            request.access_key_id,
            request.user_id,
            request.created_at,
            request.expire_at,
        )

        if not self._access_key_service.can_refresh(found_key, now):
            raise ExpiredAccessKeyError("Access key is expired")

        return RefreshResponse.from_entity(found_key, now)
