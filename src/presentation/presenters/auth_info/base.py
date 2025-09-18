__all__ = ["AuthInfoPresenter"]


from abc import abstractmethod, ABC

from presentation.models import AuthInfo, PresentedAuthInfo


class AuthInfoPresenter(ABC):

    # TODO: Create descendant for JwtInfo and Session info
    @abstractmethod
    def present(self, handler_response: AuthInfo) -> PresentedAuthInfo:
        raise NotImplementedError

    @abstractmethod
    def to_auth_info[**P, T](
        self, raw_data: T, *args: P.args, **kwargs: P.kwargs
    ) -> AuthInfo:
        raise NotImplementedError

    def validate[**P, T](self, raw_data: T, *args: P.args, **kwargs: P.kwargs) -> bool:
        self.to_auth_info(raw_data, *args, **kwargs)
        return True
