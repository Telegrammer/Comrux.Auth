import re

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID
from .base import ValueObject
from ..exceptions import DomainFieldError
from utils import extract_timestamp_from_uuid7


__all__ = ["Id", "Uuid4", "Uuid7"]


@dataclass(eq=False)
class Id[T](ValueObject):
    def __eq__(self, other) -> bool:
        return self.value == other.value


@dataclass
class Uuid4(Id[str]):

    def __post_init__(self):
        super().__post_init__()
        pattern = re.compile(
            r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
        )
        if not pattern.search(self.value):
            raise DomainFieldError("value is not an id")


@dataclass
class Uuid7(Id[str]):

    @property
    def issued_at(self) -> datetime:
        u = UUID(self.value)
        timestamp_ns = extract_timestamp_from_uuid7(u)
        # Конвертируем наносекунды в секунды (делим на 1e9)
        timestamp_s = timestamp_ns / 1_000_000_000
        return datetime.fromtimestamp(timestamp_s, tz=timezone.utc)

    def __post_init__(self):
        super().__post_init__()
        pattern = re.compile(r"^[0-9a-f]{8}(?:\-[0-9a-f]{4}){3}-[0-9a-f]{12}$")
        if not pattern.search(self.value):
            raise DomainFieldError("value is not an id")
