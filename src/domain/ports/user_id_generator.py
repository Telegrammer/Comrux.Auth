from abc import abstractmethod, ABC
from domain.value_objects import Id


__all__ = ["UserIdGenerator"]


class UserIdGenerator(ABC):

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Id:
        raise NotImplementedError
