__all__ = ["TimestampClock"]

from domain.ports import Clock
from datetime import datetime, timezone



class TimestampClock(Clock):

    def now(self) -> datetime:
        return datetime.now(timezone.utc)