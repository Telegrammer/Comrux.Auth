__all__ = ["AuthInfo", "JwtInfo", "SessionInfo"]


from pydantic import BaseModel
from datetime import datetime


class AuthInfo(BaseModel):
    key_id: str
    user_id: str | None = None
    created_at: datetime| None = None 
    expire_at: datetime | None = None


class JwtInfo(BaseModel):
    access_token: str
    refresh_token: str | None
    token_type: str


class SessionInfo(BaseModel):
    session_id: str
