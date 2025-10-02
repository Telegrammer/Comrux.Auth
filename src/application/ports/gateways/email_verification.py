__all__ = ["EmailVerificationQueryGateway", "EmailVerificationCommandGateway"]


from typing import Protocol
from abc import abstractmethod


from domain.entities import EmailVerification
from domain.value_objects import TokenHash


class EmailVerificationCommandGateway(Protocol):

    @abstractmethod
    async def add(self, verification_object: EmailVerification) -> None:
        raise NotImplementedError

    @abstractmethod
    async def handle_used(self, verification_object: EmailVerification) -> None:
        raise NotImplementedError


class EmailVerificationQueryGateway(Protocol):

    @abstractmethod
    async def by_token_hash(self, token_hash: TokenHash) -> EmailVerification:
        raise NotImplementedError
