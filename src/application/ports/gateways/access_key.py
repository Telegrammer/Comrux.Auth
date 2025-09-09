from abc import abstractmethod
from typing import Protocol, Sequence

from domain import User, AccessKey, AccessKeyId

__all__ = ["AccessKeyCommandGateway", "AccessKeyQueryGateway"]


class AccessKeyCommandGateway(Protocol):

    @abstractmethod
    async def add(self, access_key: AccessKey) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, access_key: AccessKeyId) -> None:
        raise NotImplementedError


class AccessKeyQueryGateway(Protocol):

    @abstractmethod
    async def by_id(self, access_key_id: AccessKeyId) -> AccessKey | None:
        raise NotImplementedError

    @abstractmethod
    async def by_user(self, user: User) -> Sequence[AccessKey] | None:
        raise NotImplementedError
