__all__ = ["StatefullRefreshRequest", "StatefullRefreshUsecase"]

from datetime import datetime
from dataclasses import dataclass

from domain import AccessKeyId, AccessKey, UserId, AccessKeyService
from domain.value_objects import PassedDatetime, FutureDatetime

from .contract import RefreshRequest, RefreshResponse, RefreshUsecase

from application.ports import Clock, AccessKeyQueryGateway


@dataclass(slots=True, kw_only=True, frozen=True)
class StatefullRefreshRequest(RefreshRequest):

    @classmethod
    def from_primitives(
        cls,
        *,
        key_id_primitive: str,
        user_id_primitive: str,
    ) -> "StatefullRefreshRequest":

        return cls(
            access_key_id=AccessKeyId(key_id_primitive),
            user_id=UserId(user_id_primitive),
        )


class StatefullRefreshUsecase:

    def __init__(
        self,
        clock: Clock,
        access_key_gateway: AccessKeyQueryGateway,
        access_key_service: AccessKeyService,
    ):
        self._clock: Clock = clock
        self._access_key_gateway: AccessKeyQueryGateway = access_key_gateway
        self._access_key_service: AccessKeyService = access_key_service

    async def __call__(
        self, request: StatefullRefreshRequest
    ) -> RefreshResponse | None:

        now: datetime = self._clock.now()

        found_key: AccessKey | None = await self._access_key_gateway.by_id(
            request.access_key_id.value
        )

        if not found_key:
            return None

        if found_key.user_id != request.user_id:
            return None

        if not self._access_key_service.can_refresh(found_key, now):
            return None

        return RefreshResponse.from_entity(found_key, now)
