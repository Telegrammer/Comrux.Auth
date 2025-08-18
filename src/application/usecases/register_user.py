from dataclasses import dataclass


from domain.value_objects import Email, PhoneNumber, RawPassword
from domain import User, UserService

from application.ports import UserCommandGateway

__all__ = ["RegisterUserUsecase", "RegisterUserRequest"]

@dataclass(slots=True, kw_only=True, frozen=True)
class RegisterUserRequest:
    email: Email
    phone: PhoneNumber
    raw_password: RawPassword

    @classmethod
    def from_primitives(cls, *, email: str, phone: str, password: str):
        return cls(
            email=Email(email),
            phone=PhoneNumber(phone),
            raw_password=RawPassword(password),
        )


class RegisterUserUsecase:

    def __init__(self, service: UserService, command_gateway: UserCommandGateway):
        self._user_service = service
        self._user_gateway = command_gateway

    async def __call__(
        self, request: RegisterUserRequest
    ) -> None:
        new_user: User = self._user_service.create_user(request.email, request.phone, request.raw_password)
        await self._user_gateway.add(new_user)