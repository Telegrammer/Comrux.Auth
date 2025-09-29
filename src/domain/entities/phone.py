from domain import Entity
from domain.value_objects import Uuid4, PhoneNumber

class PhoneId(Uuid4): ...

class Phone(Entity[Uuid4]):

    number: PhoneNumber
    is_verified: bool = False
