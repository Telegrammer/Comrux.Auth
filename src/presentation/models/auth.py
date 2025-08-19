__all__ = ["AuthInfo", "JwtInfo", "SessionInfo"]


from pydantic import BaseModel


class AuthInfo(BaseModel): ...


class JwtInfo(AuthInfo):
    access_token: str
    token_type: str


class SessionInfo(AuthInfo):
    session_id: str
