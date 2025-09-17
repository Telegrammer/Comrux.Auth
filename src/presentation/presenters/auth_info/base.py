from abc import abstractmethod, ABC

from presentation.models import AuthInfo

class AuthInfoPresenter(ABC):

    @abstractmethod
    def present(self, handler_response: AuthInfo) -> AuthInfo:
        raise NotImplementedError

    @abstractmethod
    def to_auth_info[**P, T](self, raw_data: T, *args: P.args, **kwargs: P.kwargs) -> AuthInfo:
        raise NotImplementedError

    def validate[T](self, raw_data: T) -> bool:
        self.to_auth_info(raw_data)
        return True
