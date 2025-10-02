__all__ = ["UrlsafeEmailVerificationTokenGenerator"]

from domain.ports import EmailVerificationTokenGenerator
from domain.value_objects import Token
from secrets import token_urlsafe


class UrlsafeEmailVerificationTokenGenerator(EmailVerificationTokenGenerator):

    def __call__(self, *args, **kwds) -> Token:
        return Token.create(token_urlsafe(32))
