from abc import abstractmethod, ABC
from domain.entities.access_key import AccessKeyId


__all__ = ["AccessKeyIdGenerator"]


class AccessKeyIdGenerator(ABC):

    @abstractmethod
    def __call__(self, *args, **kwargs) -> AccessKeyId:
        raise NotImplementedError
