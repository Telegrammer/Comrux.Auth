__all__ = ["Transaction"]


from typing import Protocol
from abc import abstractmethod


class Transaction(Protocol):
    
    @abstractmethod
    async def complete(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def cancel(self) -> None:
        raise NotImplementedError
