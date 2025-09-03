__all__ = ["RefreshRequest", "RefreshUsecase", "RefreshResponse"]

from datetime import datetime
from dataclasses import dataclass
from typing import TypedDict, Protocol
from abc import abstractmethod

from domain import UserId, AccessKeyId, AccessKey
from domain.value_objects import PassedDatetime, FutureDatetime


@dataclass(slots=True, kw_only=True, frozen=True)
class RefreshRequest(Protocol):

    access_key_id: AccessKeyId
    user_id: UserId

    @classmethod
    @abstractmethod
    def from_primitives(cls, *args, **kwargs) -> "RefreshRequest": ...


class RefreshResponse(TypedDict):
    key_id: AccessKeyId
    user_id: UserId

    updated_at: datetime

    @classmethod
    def from_entity(
        cls, entity: AccessKey, updated_at: PassedDatetime
    ) -> "RefreshResponse":
        return cls(key_id=entity.id_, user_id=entity.user_id, updated_at=updated_at)


class RefreshUsecase:

    @abstractmethod
    async def __call__(self, request: RefreshRequest) -> RefreshResponse:
        raise NotImplementedError
