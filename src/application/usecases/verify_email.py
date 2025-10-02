from datetime import datetime
from dataclasses import dataclass


from domain.entities import EmailVerification, User
from domain.ports import EmailVerificationTokenHasher
from domain.value_objects import TokenHash
from domain.services import UserService

from application.ports import (
    UserQueryGateway,
    Clock,
    UserCommandGateway,
    EmailVerificationQueryGateway,
    EmailVerificationCommandGateway,
)


@dataclass
class VerifyEmailRequest:
    raw_token: str


class VerifyEmailUsecase:

    def __init__(
        self,
        clock: Clock,
        token_hasher: EmailVerificationTokenHasher,
        user_queries: UserQueryGateway,
        user_commands: UserCommandGateway,
        user_service: UserService,
        email_verification_queries: EmailVerificationQueryGateway,
        email_verification_commands: EmailVerificationCommandGateway,
    ):
        self._clock = clock
        self._token_hasher = token_hasher
        self._user_queries = user_queries
        self._user_commands = user_commands
        self._user_service = user_service
        self._email_verification_queries = email_verification_queries
        self._email_verification_commands = email_verification_commands

    async def __call__(self, request: VerifyEmailRequest):

        now: datetime = self._clock.now()

        token_hash: TokenHash = self._token_hasher.hash(request.raw_token)
        verification_object: EmailVerification = (
            await self._email_verification_queries.by_token_hash(token_hash)
        )
        found_user: User = await self._user_gateway.by_id(verification_object.user_id)
        self._user_service.verify_email(now, found_user, verification_object)

        self._user_commands.update(found_user)
        self._email_verification_commands.handle_used(verification_object)
