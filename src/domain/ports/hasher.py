from typing import Protocol
from abc import abstractmethod
from domain.value_objects import RawPassword, PasswordHash


__all__ = ["PasswordHasher"]


class PasswordHasher(Protocol):
    @abstractmethod
    def hash(self, raw_password: RawPassword) -> PasswordHash:
        raise NotImplementedError

    @abstractmethod
    def verify(self, raw_password: RawPassword, password_hash: PasswordHash) -> bool:
        raise NotImplementedError
