from domain import User, UserService
from domain.value_objects import Email, RawPassword, PhoneNumber
from application.ports import UserCommandGateway, UserQueryGateway


__all__ = ["RegisterUserUsecase", "LoginUsecase"]


class RegisterUserUsecase:

    def __init__(self, service: UserService, command_gateway: UserCommandGateway):
        self._user_service = service
        self._user_gateway = command_gateway

    async def __call__(
        self, email: Email, phone: PhoneNumber, raw_password: RawPassword
    ) -> None:
        new_user: User = self._user_service.create_user(email, phone, raw_password)
        await self._user_gateway.add(new_user)


class LoginUsecase:

    def __init__(self, service: UserService, query_gateway: UserQueryGateway):
        self._user_service = service
        self._user_gateway = query_gateway

    async def __call__(
            self, email: Email, raw_password: RawPassword
    ) -> User | None:
        
        known_user: User | None = await self._user_gateway.by_email(email)
        if not known_user:
            return None
        return known_user
            