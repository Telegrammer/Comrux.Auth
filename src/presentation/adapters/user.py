from pydantic import BaseModel, EmailStr
from pydantic import UUID4

__all__ = ["UserCreate", "UserRead", "UserLogin"]


class BaseUser(BaseModel):
    email: EmailStr
    phone: str


class UserCreate(BaseUser):
    raw_password: str


class UserRead(BaseUser):
    id_: UUID4


class UserLogin(BaseModel):
    email: EmailStr
    raw_password: str
