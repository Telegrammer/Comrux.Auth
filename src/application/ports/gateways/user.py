from abc import abstractmethod
from typing import Protocol, Sequence

from domain import User
from domain.value_objects import Id, EmailAddress

from application.query_params.user import UserListParams

__all__ = ["UserCommandGateway", "UserQueryGateway"]


class UserCommandGateway(Protocol):

    @abstractmethod
    async def add(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user: User) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, user: User) -> None:
        raise NotImplementedError


class UserQueryGateway(Protocol):

    @abstractmethod
    async def read_all(self, params: UserListParams) -> Sequence[User]:
        raise NotImplementedError

    @abstractmethod
    async def by_id(self, user_id: Id) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def by_email(self, email: EmailAddress) -> User | None:
        raise NotImplementedError
