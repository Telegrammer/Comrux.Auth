from domain import AccessKeyId
import uuid
from domain.ports import UserIdGenerator

__all__ = ["AccessKeyUuid4Generator"]


class AccessKeyUuid4Generator(UserIdGenerator):
    def __call__(self) -> AccessKeyId:
        return AccessKeyId(str(uuid.uuid4()))
