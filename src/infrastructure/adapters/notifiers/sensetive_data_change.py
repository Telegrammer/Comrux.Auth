from application.ports import SensetiveDataChangeNotifier, SensetiveDataChangePayload
from faststream.redis import RedisBroker
from infrastructure.models.messages import UserSensetiveDataChange


class RedisStreamsSensetiveDataChangeNotifier(SensetiveDataChangeNotifier):

    def __init__(self, broker: RedisBroker):
        self._broker: RedisBroker = broker

    async def notify(self, payload: SensetiveDataChangePayload):
        await self._broker.publish(
            UserSensetiveDataChange(**payload.__dict__),
            stream="user:sensetive_data_changed",
        )
