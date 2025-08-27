

from .base import DomainError

class UserAlreadyExistsError(DomainError): ...

class UserNotFoundError(DomainError): ...