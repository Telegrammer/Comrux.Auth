from typing import Protocol
from abc import abstractmethod
from dataclasses import dataclass

from domain import UserId
from datetime import datetime


@dataclass
class SensetiveDataChangePayload:

    user_id: UserId
    changed_fields: list[str]
    occured: datetime


class SensetiveDataChangeNotifier(Protocol):

    @abstractmethod
    async def notify(self, event_info: SensetiveDataChangePayload) -> None:
        raise NotImplementedError
