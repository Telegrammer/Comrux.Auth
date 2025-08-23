__all__ = ["AccessKey", "AccessKeyId"]


from datetime import datetime
from dataclasses import dataclass


from ..value_objects import Uuid4, FutureDatetime, PassedDatetime
from .base import Entity


type AccessKeyId = Uuid4


@dataclass
class AccessKey(Entity[AccessKeyId]):

    user_id: Uuid4
    created_at: PassedDatetime
    expire_at: FutureDatetime

    def __post_init__(self):
        if self.created_at >= self.expire_at:
            raise ValueError("Access key have impossible/pointless lifetime")
