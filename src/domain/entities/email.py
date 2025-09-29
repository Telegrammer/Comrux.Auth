from dataclasses import dataclass

from domain import Entity
from domain.value_objects import Uuid4, Email as EmailAddress


class EmailId(Uuid4): ...


@dataclass
class Email(Entity[EmailId]):
    address: EmailAddress
    is_verified: bool = False
