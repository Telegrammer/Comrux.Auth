from domain import User
from domain.value_objects import Email, RawPassword, PhoneNumber
from domain import UserService
from application.ports import UserCommandGateway


__all__ = ["RegisterUserUsecase"]


class RegisterUserUsecase:

    def __init__(self, service: UserService, command_gateway: UserCommandGateway):
        self._user_service = service
        self._user_gateway = command_gateway

    async def __call__(
        self, email: Email, phone: PhoneNumber, raw_password: RawPassword
    ) -> None:
        new_user: User = self._user_service.create_user(email, phone, raw_password)
        await self._user_gateway.add(new_user)
