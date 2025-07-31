from typing import Protocol
from abc import abstractmethod
from value_objects import Id




__all__ = ["UserIdGenerator"]



class UserIdGenerator(Protocol):

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Id:
        raise NotImplementedError