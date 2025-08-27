__all__ = ["AccessKey", "AccessKeyId"]


from dataclasses import dataclass


from ..exceptions import DomainFieldError
from ..value_objects import Uuid4, PassedDatetime, FutureDatetime
from .base import Entity
from .user import UserId


class AccessKeyId(Uuid4): ...


@dataclass
class AccessKey(Entity[AccessKeyId]):
    """
    :raises DomainFieldError
    """

    user_id: UserId
    created_at: PassedDatetime
    expire_at: FutureDatetime

    def __post_init__(self):
        if self.created_at >= self.expire_at:
            raise DomainFieldError("Access key have impossible/pointless lifetime")
