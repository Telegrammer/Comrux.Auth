__all__ = ["UserId", "User"]

from dataclasses import dataclass
from ..value_objects import PhoneNumber, PasswordHash, Uuid4
from .base import AggregationRoot
from .email import Email


class UserId(Uuid4): ...


@dataclass(kw_only=True)
class User(AggregationRoot[UserId]):
    """
    :raises DomainFieldError
    """

    email: Email
    password_hash: PasswordHash
    phone: PhoneNumber
