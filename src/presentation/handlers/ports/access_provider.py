__all__ = ["AccessProvider"]

from abc import abstractmethod, ABC


from application.usecases.login_user import LoginUserResponse
from presentation.models import AuthInfo


class AccessProvider(ABC):

    @abstractmethod
    def provide(usecase_response: LoginUserResponse) -> AuthInfo:
        raise NotImplementedError
