from abc import abstractmethod, ABC
from domain.value_objects import Uuid7


__all__ = ["EmailVerificationIdGenerator"]



class EmailVerificationIdGenerator(ABC):

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Uuid7:
        raise NotImplementedError
