from typing import Protocol
from abc import abstractmethod
from domain.entities import EmailVerification
from domain.value_objects import Token, TokenHash


__all__ = ["EmailVerificationTokenHasher"]


class EmailVerificationTokenHasher(Protocol):
    @abstractmethod
    def hash(self, raw_token: Token) -> TokenHash:
        raise NotImplementedError

    @abstractmethod
    def verify(self, raw_token: Token, verification_object: EmailVerification) -> bool:
        raise NotImplementedError
