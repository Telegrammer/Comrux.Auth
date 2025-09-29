__all__ = ["PasswordLoginMethod", "PasswordLoginUserRequest"]

from dataclasses import dataclass


from domain.entities import User, AccessKey
from domain.services import UserService, AccessKeyService
from domain.value_objects import EmailAddress, RawPassword

from application.ports import Clock, UserQueryGateway
from application.exceptions.user import UserAuthenticationError

from ..contract import LoginUserRequest, LoginMethod

@dataclass(slots=True, kw_only=True, frozen=True)
class PasswordLoginUserRequest(LoginUserRequest):
    email: EmailAddress
    raw_password: RawPassword

    @classmethod
    def from_primitives(
        cls, *, email: str, password: str
    ) -> "PasswordLoginUserRequest":
        return cls(
            email=EmailAddress(email),
            raw_password=RawPassword(password),
        )


class PasswordLoginMethod(LoginMethod[PasswordLoginUserRequest]):

    def __init__(
        self,
        clock: Clock,
        user_service: UserService,
        user_gateway: UserQueryGateway,
        access_key_serivce: AccessKeyService,
    ):
        self._clock: Clock = clock
        self._user_service: UserService = user_service
        self._user_gateway: UserQueryGateway = user_gateway
        self._access_key_service: AccessKeyService = access_key_serivce

    async def __call__(self, request: PasswordLoginUserRequest) -> AccessKey:
        known_user: User = await self._user_gateway.by_email(request.email)

        if not self._user_service.is_password_valid(known_user, request.raw_password):
            raise UserAuthenticationError("given password is not valid")

        new_access_key: AccessKey = self._access_key_service.create_access_key(
            getattr(known_user, "__object_id_"), self._clock.now()
        )

        return new_access_key
