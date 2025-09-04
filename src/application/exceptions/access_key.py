from .base import UsecaseError


class ExpiredAccessKeyError(UsecaseError): ...


class AccessKeyNotFound(UsecaseError): ...
