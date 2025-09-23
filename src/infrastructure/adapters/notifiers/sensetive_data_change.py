

from dataclasses import dataclass

from application.ports import SensetiveDataChangeNotifier, SensetiveDataChangePayload
from faststream.redis import RedisBroker
from datetime import datetime

#TODO Remove payload structure to model module
@dataclass
class Payload:
    user_id: str
    changed_data_types: list[str]
    occured: datetime

class RedisStreamsSensetiveDataChangeNotifier(SensetiveDataChangeNotifier):

    def __init__(self, broker: RedisBroker):
        self._broker: RedisBroker = broker

    async def notify(self, payload: SensetiveDataChangePayload):
        
        #TODO: make payload construction in another object
        redis_payload: dict[str, str | datetime] = {
            "user_id": payload.user_id,
            "changed_fields": payload.changed_data_types,
            "occured": payload.occured
        }
        await self._broker.publish(redis_payload, stream="user:sensetive_data_changed")