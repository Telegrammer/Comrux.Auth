__all__ = ["EmailVerificationService"]


from datetime import datetime

from domain import UserId, EmailVerification
from domain.ports import EmailVerificationTokenHasher, EmailVerificationIdGenerator, EmailVerificationTokenGenerator
from domain.policies import EmailVerificationPolicy
from domain.value_objects import FutureDatetime, Token
from ..exceptions.email_verification import EmailVerificationObjectUsedError, EmailVerificationObjectExpiredError


class EmailVerificationService:

    def __init__(
            self,
            id_generator: EmailVerificationIdGenerator,
            token_generator: EmailVerificationTokenGenerator,
            hasher: EmailVerificationTokenHasher,
            verifictaion_policy: EmailVerificationPolicy,
        ):
        self._id_generator = id_generator
        self._token_generator = token_generator
        self._hasher = hasher
        self._verification_policy = verifictaion_policy

    def create_email_verification(self, now: datetime, user_id: UserId) -> EmailVerification:
        return EmailVerification(
            id_=self._id_generator(now),
            user_id=user_id,
            token_hash=self._hasher.hash(self._token_generator()),
            expire_at=FutureDatetime(now + self._verification_policy.token_ttl, now=now)
        )
    
    def _is_fresh(self, verification_object: EmailVerification, now: datetime) -> bool:
        ttl_total: int = (verification_object.expire_at - verification_object.id_.issued_at).total_seconds()
        ttl_left: int = (verification_object.expire_at - now).total_seconds()
        return (
            ttl_total > 0
            and ttl_left >= self._validity_policy.min_freshness_precentage * ttl_total
        )

    def is_token_valid(self, now: datetime, raw_token: Token, verification_object: EmailVerification) -> bool:

        if verification_object.used:
            raise EmailVerificationObjectUsedError("Token was used earlier")
        if self._is_expired(verification_object, now):
            raise EmailVerificationObjectExpiredError("Token was not used but it's lifetime ended")
        
        return self._hasher.verify(raw_token, verification_object)