
from datetime import datetime

from domain.entities import Email, EmailVerification
from .email_verification import EmailVerificationService
from domain.value_objects import EmailAddress
from domain.ports import EmailIdGenerator

from ..exceptions.email_verification import EmailVerificationTokenMismatchError


class EmailService:

    def __init__(self, id_generator: EmailIdGenerator, email_verifictaion_service: EmailVerificationService):
        self._id_generator = id_generator
        self._email_verification_service = email_verifictaion_service

    def create_email(self, address: EmailAddress) -> Email:
        return Email(id_=self._id_generator(), address=address, is_verified=False)

    def verify_email(self, now: datetime, email: Email, verification_object: EmailVerification) -> None:
        if not self._email_verification_service.is_token_valid(now, verification_object):
            raise EmailVerificationTokenMismatchError("Risky token: abort")
        
        verification_object.use(now)
        email.is_verified = True
