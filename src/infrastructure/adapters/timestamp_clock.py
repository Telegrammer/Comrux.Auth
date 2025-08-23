__all__ = ["TimestampClock"]

from application.ports import Clock
from datetime import datetime, timezone



class TimestampClock(Clock):

    def now(self) -> datetime:
        return datetime.now(timezone.utc)