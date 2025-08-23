__all__ = ["JwtAuthInfoPresenter"]

from datetime import datetime, timedelta
from typing import TypedDict, Any

from application.usecases.login_user import LoginUserResponse
from presentation.handlers.ports import AuthInfoPresenter
from presentation.models import JwtInfo

import jwt


class JwtAuthInfoPresenter(AuthInfoPresenter):
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        access_token_expiration_time: timedelta,
    ):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._access_token_expiration_time = access_token_expiration_time

    def _create_jwt_tokens(self, payloads: list[dict[str, Any]]) -> tuple[str]:
        return tuple(
            jwt.encode(payload=payload, key=self._secret_key, algorithm=self._algorithm)
            for payload in payloads
        )

    def present(self, usecase_response: LoginUserResponse) -> JwtInfo:
        iat: datetime = usecase_response.pop("created_at")
        access_exp: datetime = iat + self._access_token_expiration_time
        refresh_exp: datetime = usecase_response.pop("expire_at")

        base_payload = {
            **usecase_response,
            "sub": usecase_response.pop("key_id"),
        }

        access_payload = {**base_payload, "exp": access_exp, "iat": iat}
        refresh_payload = {**base_payload, "exp": refresh_exp, "iat": iat}

        access_token, refresh_token = self._create_jwt_tokens(
            [access_payload, refresh_payload]
        )

        return JwtInfo(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
        )
