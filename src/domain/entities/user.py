from .base import Entity
from ..value_objects import Email, PhoneNumber, PasswordHash, Uuid4
from dataclasses import dataclass


@dataclass
class User(Entity[Uuid4]):
    email: Email
    phone: PhoneNumber
    password_hash: PasswordHash
