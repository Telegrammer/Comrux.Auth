__all__ = ["error_aware", "create_error_aware_decorator"]


import inspect
from typing import Type, Callable, TypeAlias

import functools
from application.exceptions.base import ApplicationError


type ErrorFactory = Callable[[Exception], ApplicationError]


def error_aware(
    error_map: dict[type[BaseException] | frozenset[type[BaseException]], ErrorFactory],
):
    flatten_error_map: dict[type[BaseException], ErrorFactory] = {}
    for raw, factory in error_map.items():
        if isinstance(raw, frozenset):
            for err in raw:
                flatten_error_map[err] = factory
        else:
            flatten_error_map[raw] = factory

    def decorator[T, **P](func: Callable[P, T]) -> Callable[P, T]:
        def handle_error(unknown: Exception) -> None:
            excepted_error_factory = flatten_error_map.get(type(unknown), None)
            if not excepted_error_factory:
                raise
            raise excepted_error_factory(unknown) from unknown

        @functools.wraps(func)
        def sync_handler(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                handle_error(exc)

        @functools.wraps(func)
        async def async_handler(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return await func(*args, **kwargs)
            except Exception as exc:
                handle_error(exc)

        return async_handler if inspect.iscoroutinefunction(func) else sync_handler

    return decorator


def create_error_aware_decorator(
    base_error_map: dict[
        Type[Exception] | frozenset[Type[Exception]], ApplicationError
    ],
):
    def outer(default_message: str | None = None):

        def decorator(func=None, *, error_map=None):
            final_map = base_error_map.copy()
            if error_map:
                final_map.update(error_map)

            if not default_message:
                return error_aware(final_map)(func) if func else error_aware(final_map)

            factory_map = {
                k: (lambda cls: (lambda _: cls(default_message)))(v)
                for k, v in final_map.items()
            }

            return error_aware(factory_map)(func) if func else error_aware(factory_map)

        return decorator

    return outer
