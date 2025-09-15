from pydantic import BaseModel, EmailStr
from pydantic import UUID4

__all__ = [
    "UserCreate",
    "UserRead",
    "UserLogin",
    "PasswordUserLogin",
    "PasswordChange",
]


class BaseUser(BaseModel):
    email: EmailStr
    phone: str


class UserCreate(BaseUser):
    password: str


class UserRead(BaseUser):
    user_id: UUID4


class UserLogin(BaseModel): ...


class PasswordUserLogin(UserLogin):
    email: EmailStr
    password: str

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
