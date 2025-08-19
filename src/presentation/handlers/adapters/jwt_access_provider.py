__all__ = ["PyJwtAccessProvider"]

from datetime import datetime, timedelta

from application.usecases.login_user import LoginUserResponse
from presentation.handlers.ports import AccessProvider
from presentation.models import JwtInfo

import jwt


class PyJwtAccessProvider(AccessProvider):

    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        access_token_expire_minutes: int,
        now: datetime,
    ):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._access_token_expire_minutes = access_token_expire_minutes
        self._now = now

    def provide(self, usecase_response: LoginUserResponse) -> JwtInfo:
        payload: LoginUserResponse = usecase_response.copy()
        payload["sub"] = payload.pop("user_id")
        expire_datetime = self._now + timedelta(
            minutes=self._access_token_expire_minutes
        )
        payload.update(exp=expire_datetime, iat=self._now)

        access_token = jwt.encode(
            payload=payload,
            key=self._secret_key,
            algorithm=self._algorithm,
        )
        token = JwtInfo(access_token=access_token, token_type="Bearer")

        return token
