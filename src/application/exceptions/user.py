from .base import ApplicationError, UsecaseError


class UserNotFoundError(ApplicationError): ...


class UserAlreadyExistsError(ApplicationError): ...


class UserAuthenticationError(UsecaseError): ...
