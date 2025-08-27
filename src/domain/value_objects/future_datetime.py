__all__ = ["FutureDatetime"]


from .base import ValueObject
from ..exceptions import DomainFieldError
from datetime import datetime
from dataclasses import dataclass


@dataclass(init=False)
class FutureDatetime(ValueObject[datetime]):

    def __init__(self, value: datetime, now: datetime):
        self.value = value
        if now >= value:
            raise DomainFieldError(
                "The datetime value must be later than the current datetime"
            )
