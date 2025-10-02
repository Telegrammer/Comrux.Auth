__all__ = ["BcryptEmailVerificationTokenHasher"]


from domain.entities import EmailVerification
from domain.ports import EmailVerificationTokenHasher
from passlib.context import CryptContext
from domain.value_objects import Token, TokenHash


class BcryptEmailVerificationTokenHasher(EmailVerificationTokenHasher):

    def __init__(self):
        self._context = CryptContext(schemes=["bcrypt"])

    def hash(self, raw_token: Token) -> TokenHash:
        return TokenHash(self._context.hash(raw_token.value))

    def verify(self, raw_token: Token, verification_object: EmailVerification) -> bool:
        return self._context.verify(raw_token.value, verification_object.token_hash)
