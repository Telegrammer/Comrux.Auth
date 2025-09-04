__all__ = ["StatefullRefreshRequest", "StatefullRefreshUsecase"]

from datetime import datetime
from dataclasses import dataclass

from domain import AccessKeyId, AccessKey, AccessKeyService

from .contract import RefreshRequest, RefreshResponse

from application.ports import Clock, AccessKeyQueryGateway
from application.exceptions import ExpiredAccessKeyError


@dataclass(slots=True, kw_only=True, frozen=True)
class StatefullRefreshRequest(RefreshRequest):

    @classmethod
    def from_primitives(
        cls,
        **kwargs

    ) -> "StatefullRefreshRequest":

        return cls(
            access_key_id=AccessKeyId(kwargs["key_id"]),
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
    ) -> RefreshResponse:

        now: datetime = self._clock.now()

        found_key: AccessKey = await self._access_key_gateway.by_id(
            request.access_key_id.value
        )

        if not self._access_key_service.can_refresh(found_key, now):
            raise ExpiredAccessKeyError("Access key expired: need to re-login")

        return RefreshResponse.from_entity(found_key, now)
