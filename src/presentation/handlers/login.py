__all__ = ["LoginHandler"]

from application.usecases.login_user import (
    LoginUserRequest,
    LoginUsecase,
    LoginUserResponse,
)

from presentation.handlers.ports import AccessProvider
from presentation.models import UserLogin, AuthInfo


class LoginHandler:

    def __init__(self, login_usecase: LoginUsecase, access_provider: AccessProvider):
        self._login_usecase = login_usecase
        self._access_provider = access_provider

    async def __call__(self, request: UserLogin) -> AuthInfo:
        response: LoginUserResponse = await self._login_usecase(
            LoginUserRequest.from_primitives(**request.model_dump())
        )
        auth_info: AuthInfo = self._access_provider.provide(response)
        return auth_info
