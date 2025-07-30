from .base import Entity
from ..value_objects import Email, PhoneNumber, PasswordHash
from dataclasses import dataclass

@dataclass
class User(Entity):
    email: Email
    phone: PhoneNumber
    password_hash: PasswordHash
