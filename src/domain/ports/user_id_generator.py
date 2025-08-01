from abc import abstractmethod, ABC
from value_objects import Id


__all__ = ["UserIdGenerator"]


class UserIdGenerator(ABC):

    @abstractmethod
    async def __call__(self, *args, **kwargs) -> Id:
        raise NotImplementedError
