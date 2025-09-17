__all__ = [
    "RefreshTokenBuilder",
    "StatefullRefreshTokenBuilder",
    "StateLessRefreshTokenBuilder",
]


from typing import Protocol, Any
from abc import abstractmethod
from datetime import datetime


class RefreshTokenBuilder(Protocol):

    @abstractmethod
    def __call__(
        self, raw_payload: dict[str, Any], iat: datetime, exp: datetime
    ) -> dict[str, Any]:
        raise NotImplementedError


class StateLessRefreshTokenBuilder:

    def __call__(
        self, base_payload: dict[str, Any], iat: datetime, exp: datetime
    ) -> dict[str, Any]:
        return {**base_payload, "iat": iat, "exp": exp, "type": "refresh"}


class StatefullRefreshTokenBuilder:

    def __call__(
        self, base_payload: dict[str, Any], iat: datetime, exp: datetime
    ) -> dict[str, Any]:
        return {"sub": base_payload.get("sub", None), "type": "refresh"}
