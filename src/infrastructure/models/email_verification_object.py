from pydantic import BaseModel


class EmailVerificationDto(BaseModel):
    id_: str
    user_id: str
    token_hash: bytes
    expire_at: str
    used: int = 0
    used_at: str = ""
