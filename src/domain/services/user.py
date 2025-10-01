from datetime import datetime

from domain.entities import User, EmailVerification
from domain.value_objects import RawPassword, PasswordHash, EmailAddress, PhoneNumber
from domain.ports import PasswordHasher, UserIdGenerator
from .email import EmailService

class UserService:

    def __init__(
        self,
        hasher: PasswordHasher,
        id_generator: UserIdGenerator,
        email_service: EmailService,
    ):
        self._password_hasher = hasher
        self._user_id_generator = id_generator
        self._email_service = email_service

    def create_user(
        self, email: EmailAddress, phone: PhoneNumber, raw_password: RawPassword
    ) -> User:

        return User(
            id_=self._user_id_generator(),
            email=self._email_service.create_email(email),
            phone=phone,
            password_hash=self._password_hasher.hash(raw_password),
        )

    def is_password_valid(self, user: User, raw_password: RawPassword) -> bool:
        return self._password_hasher.verify(raw_password.value, user.password_hash)

    def change_password(self, user: User, new_password: RawPassword) -> None:
        new_password_hash: PasswordHash = self._password_hasher.hash(new_password)
        user.password_hash = new_password_hash

    def verify_email(self, now: datetime, user: User, verification_object: EmailVerification) -> None:
        self._email_service.verify_email(now, user.email, verification_object)
