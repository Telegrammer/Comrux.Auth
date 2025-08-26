from abc import abstractmethod, ABC
from domain.entities.user import UserId


__all__ = ["UserIdGenerator"]


class UserIdGenerator(ABC):

    @abstractmethod
    def __call__(self, *args, **kwargs) -> UserId:
        raise NotImplementedError
