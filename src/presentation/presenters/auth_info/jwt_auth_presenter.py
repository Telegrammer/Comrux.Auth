__all__ = ["JwtAuthInfoPresenter"]


from datetime import datetime, timedelta
from typing import Any

import jwt

from application.exceptions import ExpiredAccessKeyError
from presentation.exceptions import InvalidTokenTypeError


from presentation.models import JwtInfo, AuthInfo
from presentation.constans import TokenType

from .base import AuthInfoPresenter
from .refresh_token_builder import RefreshTokenBuilder


class JwtAuthInfoPresenter(AuthInfoPresenter):
    def __init__(
        self,
        token_builder: RefreshTokenBuilder,
        secret_key: str,
        public_key: str,
        algorithm: str,
        access_token_expiration_time: timedelta,
    ):
        self._token_builder: RefreshTokenBuilder = token_builder
        self._secret_key: str = secret_key
        self._public_key: str = public_key
        self._algorithm: str = algorithm
        self._access_token_expiration_time: timedelta = access_token_expiration_time

    def _encode(self, payload: dict[str, Any]) -> str:
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def _decode(self, credentials: bytes) -> dict[str, Any]:
        return jwt.decode(
            jwt=credentials, key=self._public_key, algorithms=self._algorithm
        )

    def present(self, handler_response: AuthInfo) -> JwtInfo:

        auth_info: dict = handler_response.model_dump()

        created_at: datetime = auth_info.pop("created_at")

        access_exp: datetime = created_at + self._access_token_expiration_time
        refresh_exp: datetime | None = auth_info.pop("expire_at")

        base_payload: dict[str, Any] = {
            "sub": auth_info.pop("key_id"),
            **auth_info,
        }

        access_payload = {
            **base_payload,
            "exp": access_exp,
            "iat": created_at,
            "type": TokenType.ACCESS,
        }
        access_token = self._encode(access_payload)

        refresh_token: str | None = (
            None
            if not refresh_exp
            else self._encode(
                self._token_builder(base_payload, created_at, refresh_exp)
            )
        )

        return JwtInfo(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
        )

    def to_auth_info[bytes](
        self, credentials: bytes, reqiered_type: TokenType = TokenType.ANY
    ) -> AuthInfo:
        try:
            payload: dict[str, Any] = self._decode(credentials)
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredAccessKeyError("Given Access key is expired")

        if (
            reqiered_type != TokenType.ANY
            and payload.get("type", None) != reqiered_type
        ):
            raise InvalidTokenTypeError(f"Token is not {reqiered_type}")

        return AuthInfo(
            key_id=payload["sub"],
            user_id=payload.get("user_id", None),
            created_at=payload.get("iat", None),
            expire_at=payload.get("exp", None),
        )

    def validate[bytes](self, raw_data: bytes, required_type: TokenType):
        return super().validate(raw_data, required_type)