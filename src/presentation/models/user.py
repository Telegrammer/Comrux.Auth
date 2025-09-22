from pydantic import BaseModel, EmailStr
from pydantic import UUID4
from application import (
    LoginUserRequest,
)

from application.usecases.login_user import PasswordLoginUserRequest

__all__ = [
    "UserCreate",
    "UserRead",
    "UserLogin",
    "PasswordUserLogin",
    "PasswordChange",
    "LoginUserRequestFactory",
]


class BaseUser(BaseModel):
    email: EmailStr
    phone: str


class UserCreate(BaseUser):
    password: str


class UserRead(BaseUser):
    user_id: UUID4


class UserLogin(BaseModel):

    def accept(self, visitor: "LoginUserRequestFactory") -> LoginUserRequest:
        ...


class PasswordUserLogin(UserLogin):
    email: EmailStr
    password: str

    def accept(self, visitor: "LoginUserRequestFactory") -> LoginUserRequest:
        return visitor.handlePasswordLogin(self)


class LoginUserRequestFactory:

    """
        Converts a Presentation Layer DTO (UserLogin) into the corresponding
        Application layer LoginUserRequest.
    """
    def handlePasswordLogin(self, request: PasswordUserLogin) -> LoginUserRequest:
        return PasswordLoginUserRequest.from_primitives(**request.model_dump())


class PasswordChange(BaseModel):
    current_password: str
    new_password: str
