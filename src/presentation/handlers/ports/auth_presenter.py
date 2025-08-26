__all__ = ["AuthInfoPresenter"]

from abc import abstractmethod, ABC


from application.usecases.login_user import LoginUserResponse
from presentation.models import AuthInfo


class AuthInfoPresenter(ABC):

    @abstractmethod
    def present(usecase_response: LoginUserResponse) -> AuthInfo:
        raise NotImplementedError
