__all__ = ["GetCurrentUserUsecase", "GetCurrentUserResponse"]


from typing import TypedDict
from domain import UserId, User
from domain.value_objects import Email, PhoneNumber
from application.services import CurrentUserService


class GetCurrentUserResponse(TypedDict):

    user_id: UserId
    email: Email
    phone: PhoneNumber

    @classmethod
    def from_entity(cls, entity: User) -> "GetCurrentUserResponse":
        return cls(user_id=entity.id_, email=entity.email, phone=entity.phone)


class GetCurrentUserUsecase:

    def __init__(self, current_user_service: CurrentUserService):
        self._current_user_service: CurrentUserService = current_user_service

    async def __call__(self) -> GetCurrentUserResponse:
        return GetCurrentUserResponse.from_entity(await self._current_user_service())
