from domain import UserId
import uuid
from domain.ports import UserIdGenerator

__all__ = ["UserUuid4Generator"]


class UserUuid4Generator(UserIdGenerator):
    def __call__(self, *args, **kwargs) -> UserId:
        return UserId(str(uuid.uuid4()))
