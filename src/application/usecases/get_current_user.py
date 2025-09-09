__all__ = ["GetCurrentUserRequest", "GetCurrentUserUsecase", "GetCurrentUserResponse"]


from dataclasses import dataclass
from typing import TypedDict
from domain import UserId, User
from domain.value_objects import Email, PhoneNumber
from application.ports import UserQueryGateway


@dataclass
@dataclass
class GetCurrentUserRequest:
    user_id: UserId

    @classmethod
    def from_primitives(cls, *, user_id: str, **_: object) -> "GetCurrentUserRequest":
        return cls(user_id=UserId(user_id))


class GetCurrentUserResponse(TypedDict):

    user_id: UserId
    email: Email
    phone: PhoneNumber

    @classmethod
    def from_entity(cls, entity: User) -> "GetCurrentUserResponse":
        return cls(user_id=entity.id_, email=entity.email, phone=entity.phone)


class GetCurrentUserUsecase:

    def __init__(self, user_gateway: UserQueryGateway):
        self._user_gateway: UserQueryGateway = user_gateway

    async def __call__(self, request: GetCurrentUserRequest) -> GetCurrentUserResponse:
        found_user: User = await self._user_gateway.by_id(request.user_id.value)
        return GetCurrentUserResponse.from_entity(found_user)
