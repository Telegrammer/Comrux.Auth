__all__ = ["PassedDatetime"]


from .base import ValueObject
from datetime import datetime
from dataclasses import dataclass


@dataclass(init=False)
class PassedDatetime(ValueObject[datetime]):

    def __init__(self, value: datetime, now: datetime):
        self.value = value
        if now < value:
            raise ValueError(
                "The datetime value must be earlier than the current datetime"
            )
