from dataclasses import dataclass
from typing import TypedDict

from domain.value_objects import Email, PhoneNumber, RawPassword, Uuid4
from domain import User, UserService

from application.ports import UserQueryGateway

__all__ = ["LoginUserRequest", "LoginUserResponse", "LoginUsecase"]

@dataclass(slots=True, kw_only=True, frozen=True)
class LoginUserRequest:
    email: Email
    raw_password: RawPassword

    @classmethod
    def from_primitives(cls, *, email: str, password: str):
        return cls(
            email=Email(email),
            raw_password=RawPassword(password),
        )


class LoginUserResponse(TypedDict):
    user_id: Uuid4
    email: Email
    phone: PhoneNumber

    @classmethod
    def from_entity(cls, user: User):
        return cls(user_id=user.id_, email=user.email, phone=user.phone)


class LoginUsecase:

    def __init__(self, service: UserService, query_gateway: UserQueryGateway):
        self._user_service = service
        self._user_gateway = query_gateway

    async def __call__(self, request: LoginUserRequest) -> LoginUserResponse | None:
        

        known_user: User | None = await self._user_gateway.by_email(request.email.value)
        if not known_user:
            return None

        return (
            LoginUserResponse.from_entity(known_user)
            if self._user_service.is_password_valid(
                known_user, request.raw_password
            )
            else None
        )
