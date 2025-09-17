__all__ = ["RefreshHandler"]

from application.usecases import (
    RefreshRequest,
    RefreshUsecase,
    RefreshResponse,
)

from presentation.presenters import AuthInfoPresenter
from presentation.models import AuthInfo


class RefreshHandler:

    def __init__(
        self, request_type: type[RefreshRequest], refresh_usecase: RefreshUsecase, auth_presenter: AuthInfoPresenter
    ):
        self._request_type = request_type
        self._refresh_usecase = refresh_usecase
        self._auth_presenter = auth_presenter

    async def __call__(self, request: AuthInfo) -> AuthInfo:
        response: RefreshResponse = await self._refresh_usecase(
            self._request_type.from_primitives(**request.model_dump())
        )

        auth_info: AuthInfo = AuthInfo(
            key_id=response["key_id"],
            user_id=response["user_id"],
            created_at=response["updated_at"],
            expire_at=None,
        )

        return self._auth_presenter.present(auth_info)
