from domain import EmailId
import uuid
from domain.ports import EmailIdGenerator

__all__ = ["EmailUuid4Generator"]


class EmailUuid4Generator(EmailIdGenerator):
    def __call__(self) -> EmailId:
        return EmailId(str(uuid.uuid4()))