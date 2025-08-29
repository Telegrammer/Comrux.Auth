__all__ = ["JwtAuthInfoPresenter"]


from datetime import datetime, timedelta
from typing import Any

import jwt

from application.exceptions import ExpiredAccessKeyError
from presentation.exceptions import InvalidTokenTypeError

from presentation.handlers.ports import AuthInfoPresenter
from presentation.models import JwtInfo, AuthInfo


class JwtAuthInfoPresenter(AuthInfoPresenter):
    def __init__(
        self,
        secret_key: str,
        public_key: str,
        algorithm: str,
        access_token_expiration_time: timedelta,
    ):
        self._secret_key = secret_key
        self._public_key = public_key
        self._algorithm = algorithm
        self._access_token_expiration_time = access_token_expiration_time

    def _encode(self, payload: dict[str, Any]) -> str:
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def _decode(self, credentials: bytes) -> dict[str, Any]:
        return jwt.decode(jwt=credentials, key=self._public_key, algorithms=self._algorithm)

    def present(self, usecase_response: AuthInfo) -> JwtInfo:

        auth_info: dict = usecase_response.model_dump()

        created_at: datetime = auth_info.pop("created_at")
        access_exp: datetime = created_at + self._access_token_expiration_time
        refresh_exp: datetime | None = auth_info.pop("expire_at")

        base_payload: dict[str, Any] = {
            "sub": auth_info.pop("key_id"),
            **auth_info,
        }

        access_payload = {**base_payload, "exp": access_exp, "iat": created_at, "type": "access"}
        access_token = self._encode(access_payload)

        refresh_token: str | None = None
        if refresh_exp is not None:
            refresh_payload = {**base_payload, "exp": refresh_exp, "iat": created_at, "type": "refresh"}
            refresh_token = self._encode(refresh_payload)

        return JwtInfo(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
        )

    def to_auth_info(self, credentials: bytes, required_type: str) -> AuthInfo:
        try:
            payload: dict[str, Any] = self._decode(credentials)
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredAccessKeyError("Given Access key is expired")
    
        if payload.get("type", None) != required_type:
            raise InvalidTokenTypeError("Token is not refresh")
 
        return AuthInfo(
            key_id=payload["sub"],
            user_id=payload["user_id"],
            created_at=payload["iat"],
            expire_at=payload["exp"],
        )
