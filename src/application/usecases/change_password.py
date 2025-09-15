__all__ = ["BasicChangePasswordRequest", "BasicChangePasswordUsecase"]


from dataclasses import dataclass


from domain import User, UserService
from domain.value_objects import RawPassword


from application.ports import UserQueryGateway, UserCommandGateway
from application.exceptions import WrongPasswordError
from application.services import CurrentUserService


@dataclass
class BasicChangePasswordRequest:

    current_password: RawPassword
    new_password: RawPassword

    @classmethod
    def from_primitives(
        cls, *, current_password: str, new_password: str, **_: object
    ) -> "BasicChangePasswordRequest":
        return cls(
            current_password=RawPassword(current_password),
            new_password=RawPassword(new_password),
        )


class BasicChangePasswordUsecase:

    def __init__(
        self,
        user_service: UserService,
        user_commands: UserCommandGateway,
        user_queries: UserQueryGateway,
        current_user_service: CurrentUserService
    ):
        self._user_service = user_service
        self._user_commands = user_commands
        self._user_queries = user_queries
        self._current_user_service = current_user_service

    async def __call__(self, request: BasicChangePasswordRequest):

        current_user: User = await self._current_user_service()

        if request.current_password == request.new_password:
            raise WrongPasswordError("Password must be new")
        
        if not self._user_service.is_password_valid(current_user, request.current_password):
            raise WrongPasswordError("Incorrect password")
        
        self._user_service.change_password(current_user, request.new_password)
        await self._user_commands.update(current_user)
