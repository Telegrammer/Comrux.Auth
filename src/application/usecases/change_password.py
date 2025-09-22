__all__ = ["BasicChangePasswordRequest", "BasicChangePasswordUsecase"]


from dataclasses import dataclass
from datetime import datetime

from domain import User, UserService
from domain.value_objects import RawPassword


from application.ports import (
    UserCommandGateway,
    SensetiveDataChangeNotifier,
    SensetiveDataChangePayload,
    Clock,
)
from application.exceptions import WrongPasswordError
from application.services import CurrentUserService


@dataclass
class BasicChangePasswordRequest:

    current_password: RawPassword
    new_password: RawPassword
    logout_all_after: bool

    @classmethod
    def from_primitives(
        cls, *, current_password: str, new_password: str, logout_all: bool, **_: object
    ) -> "BasicChangePasswordRequest":
        return cls(
            current_password=RawPassword(current_password),
            new_password=RawPassword(new_password),
            logout_all_after=logout_all,
        )


class BasicChangePasswordUsecase:

    def __init__(
        self,
        clock: Clock,
        user_service: UserService,
        user_commands: UserCommandGateway,
        current_user_service: CurrentUserService,
        notifier: SensetiveDataChangeNotifier,
    ):
        self._clock = clock
        self._user_service = user_service
        self._user_commands = user_commands
        self._current_user_service = current_user_service
        self._notifier = notifier

    async def __call__(self, request: BasicChangePasswordRequest):

        now: datetime = self._clock.now()
        current_user: User = await self._current_user_service()

        if request.current_password == request.new_password:
            raise WrongPasswordError("Password must be new")

        if not self._user_service.is_password_valid(
            current_user, request.current_password
        ):
            raise WrongPasswordError("Incorrect password")

        self._user_service.change_password(current_user, request.new_password)
        await self._user_commands.update(current_user)

        if request.logout_all_after:
            await self._notifier.notify(
                SensetiveDataChangePayload(current_user.id_, ("password"), now)
            )
