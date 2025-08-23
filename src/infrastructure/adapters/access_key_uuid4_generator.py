from domain.value_objects import Uuid4
from domain import AccessKeyId
import uuid
from domain.ports import UserIdGenerator

__all__ = ["AccessKeyUuid4Generator"]


class AccessKeyUuid4Generator(UserIdGenerator):
    def __call__(self) -> AccessKeyId:
        return Uuid4(str(uuid.uuid4()))
