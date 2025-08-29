__all__ = ["PasswordLoginUsecase", "PasswordLoginUserRequest"]

from dataclasses import dataclass


from domain.entities import User, AccessKey
from domain.services import AccessKeyService, UserService
from domain.value_objects import Email, RawPassword
from .contract import LoginUserRequest, LoginUsecase, LoginUserResponse
from application.ports import Clock, UserQueryGateway
from application.exceptions.user import UserAuthenticationError


@dataclass(slots=True, kw_only=True, frozen=True)
class PasswordLoginUserRequest(LoginUserRequest):
    email: Email
    raw_password: RawPassword

    @classmethod
    def from_primitives(
        cls, *, email: str, password: str
    ) -> "PasswordLoginUserRequest":
        return cls(
            email=Email(email),
            raw_password=RawPassword(password),
        )


class PasswordLoginUsecase(LoginUsecase):

    def __init__(
        self,
        clock: Clock,
        user_service: UserService,
        user_gateway: UserQueryGateway,
        access_key_service: AccessKeyService,
    ):
        self._clock: Clock = clock
        self._user_service: UserService = user_service
        self._user_gateway: UserQueryGateway = user_gateway
        self._access_key_service: AccessKeyService = access_key_service

    async def __call__(self, request: PasswordLoginUserRequest) -> LoginUserResponse:
        known_user: User = await self._user_gateway.by_email(request.email.value)

        if not self._user_service.is_password_valid(known_user, request.raw_password):
            raise UserAuthenticationError("given password is not valid")

        new_access_key: AccessKey = self._access_key_service.create_access_key(
            user_id=getattr(known_user, "__object_id_"), now=self._clock.now()
        )
        return LoginUserResponse.from_entity(new_access_key)
