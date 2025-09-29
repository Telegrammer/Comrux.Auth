__all__ = ["UserId", "User"]

from .base import AggregationRoot
from ..value_objects import Email, PhoneNumber, PasswordHash, Uuid4
from dataclasses import dataclass


class UserId(Uuid4): ...


@dataclass
class User(AggregationRoot[UserId]):
    """
    :raises DomainFieldError
    """

    email: Email
    password_hash: PasswordHash
    phone: PhoneNumber
