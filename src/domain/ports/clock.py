__all__ = ["Clock"]


from typing import Protocol
from abc import abstractmethod
from datetime import datetime

class Clock(Protocol):

    @abstractmethod
    def now(self) -> datetime:
        raise NotImplementedError