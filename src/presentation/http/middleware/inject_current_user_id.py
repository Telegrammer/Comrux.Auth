__all__ = ["InjectCurrentUserIdMiddleware"]


from typing import Awaitable, Callable, Optional, Type

from dishka import AsyncContainer, DependencyKey
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp



from domain import UserId
from presentation.handlers.adapters.presenters import JwtAuthInfoPresenter
from presentation.handlers.ports.presenters import AuthInfoPresenter
from presentation.models import AuthInfo
from .update_context import update_context

class InjectCurrentUserIdMiddleware(BaseHTTPMiddleware):


    def __init__(
        self,
        app: ASGIApp,
        dispatch: Optional[Callable[[Request, Callable[[Request], Awaitable[Response]]], Awaitable[Response]]] = None,
    ) -> None:
        self._presenter: AuthInfoPresenter = None
        super().__init__(app, dispatch=update_context(self.dispatch))
    

    async def dispatch(self, request: Request) -> dict[DependencyKey, object | Type]:

        #TODO: encapsulate HTTPCredentials into another object 
        auth_header: str = request.headers.get("Authorization")

        if not (auth_header and auth_header.startswith("Bearer")):
            return {}
        
        credentials: bytes = auth_header.replace("Bearer ", "").encode()

        if not self._presenter:
            app_container: AsyncContainer = request.app.state.dishka_container
            self._presenter = await app_container.get(AuthInfoPresenter)

        auth_info: AuthInfo = self._presenter.to_auth_info(credentials, "any")
        if not auth_info.user_id:
            return {}

        return {UserId: UserId(auth_info.user_id)}