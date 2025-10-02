__all__ = ["Uuid7EmailVerificationIdGenerator"]


from utils import uuid7
from datetime import datetime

from domain.ports import EmailVerificationIdGenerator
from domain.value_objects import Uuid7


class Uuid7EmailVerificationIdGenerator(EmailVerificationIdGenerator):

    def __call__(self, now: datetime) -> Uuid7:
        return Uuid7(str(uuid7()))
