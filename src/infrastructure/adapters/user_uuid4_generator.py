from domain.value_objects import Uuid4, Id
import uuid
from domain.ports import UserIdGenerator

__all__ = ["UserUuid4Generator"]


class UserUuid4Generator(UserIdGenerator):
    def __call__(self, *args, **kwargs) -> Id:
        return Uuid4(str(uuid.uuid4()))
