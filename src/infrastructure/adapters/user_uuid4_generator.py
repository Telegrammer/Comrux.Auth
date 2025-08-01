from domain.value_objects import Uuid4, Id
import uuid
from domain.ports import UserIdGenerator

class UserUuid4Generator(UserIdGenerator):
    async def __call__(self, *args, **kwargs) -> Id:
        return Uuid4(str(uuid.uuid4()))

