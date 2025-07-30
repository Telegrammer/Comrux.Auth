from dataclasses import dataclass
from .base import ValueObject
import re

__all__ = ["Email"]


@dataclass
class Email(ValueObject[str]):
    def __post_init__(self):
        super().__post_init__()
        pattern: re.Pattern = re.compile(
            r"""^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"""
        )
        if not pattern.search(self.value):
            raise TypeError("Value is not an email")
