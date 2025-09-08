__all__ = ["decode"]


from typing import Callable, Sequence


def decode[**P, T](query_command: Callable[P, T]) -> Callable[P, T]:

    async def wrapper(
        *args: P.args, **kwargs: P.kwargs
    ) -> list[dict[str, str]] | dict[str, str]:
        response: Sequence[dict[bytes, bytes]] = await query_command(*args, **kwargs)

        result: list[dict[str, str]] = [
            {k.decode(): v.decode() for k, v in raw.items()} for raw in response
        ]
        return result[0] if len(result) == 1 else result

    return wrapper
