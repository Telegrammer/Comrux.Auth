from .base import AuthInfoExtractor
from presentation.handlers.ports.presenters import AuthInfoPresenter
from presentation.models import AuthInfo
from starlette.requests import Request
from dishka import AsyncContainer


class BearerAuthInfoExtractor(AuthInfoExtractor):

    def __init__(self, auth_info_presenter: AuthInfoPresenter):
        self._presenter: AuthInfoPresenter = auth_info_presenter

    async def __call__(self, request: Request) -> AuthInfo | None:
        auth_header: str = request.headers.get("Authorization")

        if not (auth_header and auth_header.startswith("Bearer ")):
            return None

        credentials: bytes = auth_header.replace("Bearer ", "").encode()
        return self._presenter.to_auth_info(credentials)
