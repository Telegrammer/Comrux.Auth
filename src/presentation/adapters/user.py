from pydantic import BaseModel, EmailStr
from pydantic import UUID4

__all__ = ["UserCreate", "UserRead"]


class BaseUser(BaseModel):
    email: EmailStr
    phone: str


class UserCreate(BaseUser):
    password: str


class UserRead(BaseUser):
    id_: UUID4
