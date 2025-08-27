import re
from dataclasses import dataclass
from .base import ValueObject
from ..exceptions import DomainFieldError

__all__ = ["PhoneNumber"]


@dataclass
class PhoneNumber(ValueObject[str]):
    def __post_init__(self):
        super().__post_init__()
        pattern: re.Pattern = re.compile(
            r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$"
        )
        if not pattern.search(self.value):
            raise DomainFieldError("value is not a phone number")
