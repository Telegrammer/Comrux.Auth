__all__ = ["update_context"]

from functools import wraps
from starlette.requests import Request
from starlette.responses import Response
from typing import Callable, Awaitable, Type
from utils.merge_context import merge_context

from dishka import AsyncContainer, DependencyKey


def update_context(
    dispatch: Callable[
        [Request, Callable[[Request], Awaitable[Response]]],
        Awaitable[dict[DependencyKey, object | Type]],
    ],
):

    @wraps(dispatch)
    async def wrapper(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:

        prev_container: AsyncContainer = request.state.dishka_container
        app_container: AsyncContainer = prev_container.parent_container

        new_context: dict[DependencyKey, object | Type] = await dispatch(request) or {}

        async with app_container(
            context=merge_context(prev_container, new_context)
        ) as request_container:
            request.state.dishka_container = request_container
            return await call_next(request)

    return wrapper
