__all__ = ["LoginUserRequest", "LoginUsecase", "LoginUserResponse", "LoginMethod"]

from dataclasses import dataclass
from typing import TypedDict, Protocol
from abc import abstractmethod, ABC

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
            expire_at=entity.expire_at,
        )


class LoginMethod:

    @abstractmethod
    async def __call__(self, request: LoginUserRequest) -> AccessKey:
        raise NotImplementedError


class LoginUsecase(ABC):

    def __init__(self, login_method: LoginMethod):
        self._core: LoginMethod = login_method


    @abstractmethod
    async def __call__(self, request: LoginUserRequest) -> LoginUserResponse:
        raise NotImplementedError
