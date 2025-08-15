from pydantic import BaseModel, EmailStr
from pydantic import UUID4

__all__ = ["UserCreate", "UserRead", "UserLogin"]

class BaseUser(BaseModel):
    email: EmailStr
    phone: str
        

class UserCreate(BaseUser):
    password: str

class UserRead(BaseUser):
    user_id: UUID4

class UserLogin(BaseModel):
    email: EmailStr
    password: str