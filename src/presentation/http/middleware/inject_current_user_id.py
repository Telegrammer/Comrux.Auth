__all__ = ["InjectCurrentUserIdMiddleware"]


from typing import Awaitable, Callable, Optional, TypeVar

from dishka import AsyncContainer
from fastapi import FastAPI, Request
from starlette.datastructures import State
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp



from domain import UserId
from application.services import CurrentUserService
from presentation.handlers.adapters.presenters import JwtAuthInfoPresenter
from presentation.models import AuthInfo




class InjectCurrentUserIdMiddleware(BaseHTTPMiddleware):


    def __init__(
        self,
        app: ASGIApp,
        dispatch: Optional[Callable[[Request, Callable[[Request], Awaitable[Response]]], Awaitable[Response]]] = None,
    ) -> None:
        super().__init__(app, dispatch=dispatch)
    

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:

        #TODO: encapsulate HTTPCredentials into another object 
        auth_header: str = request.headers.get("Authorization")

        if not auth_header:
            return await call_next(request)
        
        if not auth_header.startswith("Bearer"):
            return await call_next(request)
        
        credentials: bytes = auth_header.replace("Bearer ", "").encode()

        app_container: AsyncContainer = request.app.state.dishka_container
        presenter: JwtAuthInfoPresenter = await app_container.get(JwtAuthInfoPresenter)

        auth_info: AuthInfo = presenter.to_auth_info(credentials, "any")
        if not auth_info.user_id:
            return await call_next(request)

        user_id: UserId = UserId(auth_info.user_id)

        async with app_container(context={UserId: user_id}) as request_container:
            request.state.dishka_container = request_container
            return await call_next(request)