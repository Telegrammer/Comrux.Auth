__all__ = ["SendEmailVerificationLinkUsecase", "SendEmailVerificationRequest"]

from datetime import datetime
from dataclasses import dataclass

from domain.entities import UserId, EmailVerification, User
from domain.services import EmailVerificationService

from application.ports import Clock, EmailVerificationCommandGateway, UserQueryGateway


@dataclass
class SendEmailVerificationRequest:
    user_id: UserId

    @classmethod
    def from_primitives(cls, user_id: str) -> "SendEmailVerificationRequest":
        return cls(
            user_id=UserId(user_id)
        )


#TODO: send email to target after email verification adding
class SendEmailVerificationLinkUsecase:

    def __init__(
        self,
        clock: Clock,
        user_gateway: UserQueryGateway,
        email_verification_serivce: EmailVerificationService,
        email_verification_gateway: EmailVerificationCommandGateway,
    ):
        self._clock = clock
        self._user_gateway = user_gateway
        self._email_verification_service = email_verification_serivce
        self._email_verification_gateway = email_verification_gateway

    async def __call__(self, request: SendEmailVerificationRequest):

        now: datetime = self._clock.now()
        given_user: User = await self._user_gateway.by_id(request.user_id.value)
        verification_object: EmailVerification = (
            self._email_verification_service.create_email_verification(
                now=now, user_id=getattr(given_user, "__object_id_")
            )
        )
        await self._email_verification_gateway.add(verification_object)
