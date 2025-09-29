from abc import abstractmethod, ABC
from domain.entities.email import EmailId


__all__ = ["EmailIdGenerator"]



class EmailIdGenerator(ABC):

    @abstractmethod
    def __call__(self, *args, **kwargs) -> EmailId:
        raise NotImplementedError
