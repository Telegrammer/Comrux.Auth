from domain import AccessKeyId
import uuid
from domain.ports import AccessKeyIdGenerator

__all__ = ["AccessKeyUuid4Generator"]


class AccessKeyUuid4Generator(AccessKeyIdGenerator):
    def __call__(self) -> AccessKeyId:
        return AccessKeyId(str(uuid.uuid4()))
