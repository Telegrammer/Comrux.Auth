from dataclasses import dataclass
from .base import ValueObject
from ..exceptions import DomainFieldError
import re

__all__ = ["EmailAddress"]


@dataclass
class EmailAddress(ValueObject[str]):
    def __post_init__(self):
        super().__post_init__()
        pattern: re.Pattern = re.compile(
            r"""^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"""
        )
        if not pattern.search(self.value):
            raise DomainFieldError("Value is not an email")
