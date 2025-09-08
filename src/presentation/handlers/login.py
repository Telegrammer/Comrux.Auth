__all__ = ["LoginHandler"]


from application.ports import UnitOfWork

from application.usecases import (
    LoginUserResponse,
)

from presentation.models import UserLogin, AuthInfo

from .ports import AuthInfoPresenter, LoginUsecaseFactory


class LoginHandler:

    def __init__(
        self,
        usecase_factory: LoginUsecaseFactory,
        auth_presenter: AuthInfoPresenter,
        unit_of_work: UnitOfWork,
    ):
        self._usecase_factory = usecase_factory
        self._auth_presenter = auth_presenter
        self._unit_of_work = unit_of_work

    async def __call__(self, request: UserLogin) -> AuthInfo:

        usecase, usecase_request = self._usecase_factory(request)

        async with self._unit_of_work:
            response: LoginUserResponse = await usecase(usecase_request)

        auth_info: AuthInfo = AuthInfo(**response)
        return self._auth_presenter.present(auth_info)
