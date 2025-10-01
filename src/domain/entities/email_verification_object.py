__all__ = ["EmailVerification"]


from dataclasses import dataclass
from datetime import datetime

from ..exceptions import DomainError
from ..value_objects import Uuid7, FutureDatetime
from .base import Entity
from .user import UserId


@dataclass
class EmailVerification(Entity[Uuid7]):
    """
    :raises DomainFieldError
    """

    user_id: UserId
    expire_at: FutureDatetime
    token_hash: bytes
    used: bool = False
    used_at: datetime = None

    def __post_init__(self):
        if self.id_.issued_at >= self.expire_at:
            raise DomainError(
                "Email verification object have impossible/pointless lifetime"
            )
        
        if self.used and self.used_at is None:
            raise DomainError(
                "Email verification must have timestamp of being used if it happend"
            )
    
    def use(self, now: datetime) -> None:
        self.used = True
        self.used_at = now