__all__ = ["Email", "EmailId"]


from dataclasses import dataclass

from .base import Entity
from domain.value_objects import Uuid4, EmailAddress


class EmailId(Uuid4): ...


@dataclass
class Email(Entity[EmailId]):
    address: EmailAddress
    is_verified: bool = False
