from domain.ports import PasswordHasher
from domain.value_objects import RawPassword, PasswordHash
from passlib.context import CryptContext


__all__ = ["BcryptPasswordHasher"]


class BcryptPasswordHasher(PasswordHasher):

    def __init__(self):
        self.pwd_context: CryptContext = CryptContext(schemes=["bcrypt"])

    def hash(self, raw_password: RawPassword) -> PasswordHash:
        return PasswordHash.create(
            bytes(self.pwd_context.hash(raw_password.value), encoding="utf-8")
        )

    def verify(self, raw_password: RawPassword, password_hash: PasswordHash) -> bool:
        return self.pwd_context.verify(raw_password, password_hash)
