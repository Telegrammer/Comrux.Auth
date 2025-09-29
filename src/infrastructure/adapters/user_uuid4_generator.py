__all__ = ["UserUuid4Generator"]

import uuid
from domain import UserId
from domain.ports import UserIdGenerator


class UserUuid4Generator(UserIdGenerator):
    def __call__(self, *args, **kwargs) -> UserId:
        return UserId(str(uuid.uuid4()))
