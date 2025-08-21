__all__ = ["LoginHandler"]

from application.usecases.login_user import (
    LoginUserRequest,
    LoginUsecase,
    LoginUserResponse,
)

from presentation.handlers.ports import AuthInfoPresenter
from presentation.models import UserLogin, AuthInfo


class LoginHandler:

    def __init__(self, login_usecase: LoginUsecase, auth_presenter: AuthInfoPresenter):
        self._login_usecase = login_usecase
        self._auth_presenter = auth_presenter

    async def __call__(self, request: UserLogin) -> AuthInfo:
        response: LoginUserResponse = await self._login_usecase(
            LoginUserRequest.from_primitives(**request.model_dump())
        )
        return self._auth_presenter.present(response)
