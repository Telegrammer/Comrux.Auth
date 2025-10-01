__all__ = ["EmailVerificationTokenGenerator"]


from abc import ABC, abstractmethod
from domain.value_objects import Token


class EmailVerificationTokenGenerator(ABC):

    @abstractmethod
    def __call__(self, *args, **kwds) -> Token:
        raise NotImplementedError
