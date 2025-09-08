__all__ = ["LoginUsecaseFactory"]


from application import (
    LoginUsecase,
    LoginUserRequest,
    LoginMethod,
)

from presentation.models import UserLogin

from typing import Any, Callable, Type


class LoginUsecaseFactory:

    def __init__(
        self,
        usecase_constructor: Callable[[LoginMethod], LoginUsecase],
        method_register: dict[
            Type[UserLogin], tuple[LoginMethod, Type[LoginUserRequest]]
        ],
    ):
        self._usecase_constructor = usecase_constructor
        self._method_register = method_register

    def __call__(self, request: UserLogin) -> tuple[LoginUsecase, LoginUserRequest]:
        """
        Converts a Presentation Layer DTO (UserLogin) into the corresponding
        Application Layer LoginUsecase and LoginUserRequest.
        """

        params: dict[str, Any] = request.model_dump()

        request_type: Type[UserLogin] = type(request)

        usecase_method, usecase_request = self._method_register.get(request_type)
        return self._usecase_constructor(usecase_method), usecase_request.from_primitives(**params)
