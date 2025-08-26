__all__ = ["LoginUserRequest", "LoginUsecase", "LoginUserResponse"]

from dataclasses import dataclass
from typing import TypedDict, Protocol
from abc import abstractmethod

from domain import UserId, AccessKeyId, AccessKey
from domain.value_objects import PassedDatetime, FutureDatetime


@dataclass(slots=True, kw_only=True, frozen=True)
class LoginUserRequest(Protocol):
    @classmethod
    @abstractmethod
    def from_primitives(cls, *args, **kwargs) -> "LoginUserRequest": ...


class LoginUserResponse(TypedDict):
    key_id: AccessKeyId
    user_id: UserId
    created_at: PassedDatetime
    expire_at: FutureDatetime

    @classmethod
    def from_entity(cls, entity: AccessKey) -> "LoginUserResponse":
        return cls(
            key_id=entity.id_,
            user_id=entity.user_id,
            created_at=entity.created_at,
            expire_at=entity.expire_at
        )


class LoginUsecase:

    @abstractmethod
    async def __call__(self, request: LoginUserRequest) -> LoginUserResponse | None: ...

