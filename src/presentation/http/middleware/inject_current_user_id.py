__all__ = ["InjectCurrentUserIdMiddleware"]


from typing import Awaitable, Callable, Optional, Type

from dishka import AsyncContainer, DependencyKey
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp



from domain import UserId

from presentation.presenters import AuthInfoPresenter
from presentation.models import AuthInfo

from .extratctors import AuthInfoExtractor
from .update_context import update_context

class InjectCurrentUserIdMiddleware(BaseHTTPMiddleware):


    def __init__(
        self,
        app: ASGIApp,
        dispatch: Optional[Callable[[Request, Callable[[Request], Awaitable[Response]]], Awaitable[Response]]] = None,
    ) -> None:
        self._auth_info_extractor: AuthInfoExtractor = None
        super().__init__(app, dispatch=update_context(self.dispatch))
    

    async def dispatch(self, request: Request) -> dict[DependencyKey, object | Type]:

        if not self._auth_info_extractor:
            app_container: AsyncContainer = request.app.state.dishka_container
            self._auth_info_extractor = await app_container.get(AuthInfoExtractor)

        auth_info: AuthInfo | None = await self._auth_info_extractor(request)
        if not (auth_info and auth_info.user_id):
            return {}

        return {UserId: UserId(auth_info.user_id)}