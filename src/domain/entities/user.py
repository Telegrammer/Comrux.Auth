__all__ = ["UserId", "User"]

from .base import Entity
from ..value_objects import Email, PhoneNumber, PasswordHash, Uuid4
from dataclasses import dataclass


class UserId(Uuid4): ...


@dataclass
class User(Entity[UserId]):
    email: Email
    phone: PhoneNumber
    password_hash: PasswordHash
