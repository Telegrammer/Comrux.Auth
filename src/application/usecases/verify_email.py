


from datetime import datetime
from dataclasses import dataclass


from domain.entities import EmailVerification, User
from domain.ports import EmailVerificationTokenHasher
from domain.value_objects import TokenHash
from domain.services import UserService

from application.ports import UserQueryGateway, Clock

@dataclass
class VerifyEmailRequest:
    raw_token: str



class EmailVerificationQueryGateway:

    def by_token_hash(token_hash: TokenHash) -> EmailVerification:
        ...


class VerifyEmailUsecase:


    def __init__(self,
                 clock: Clock,
                 token_hasher: EmailVerificationTokenHasher,
                 user_gateway: UserQueryGateway,
                 user_service: UserService,
                 email_verification_gateway: EmailVerificationQueryGateway,
                ):
        self._clock = clock
        self._token_hasher = token_hasher
        self._user_gateway = user_gateway
        self._user_service = user_service
        self._email_verification_gateway = email_verification_gateway


    async def __call__(self, request: VerifyEmailRequest):
        
        now: datetime = self._clock.now()

        token_hash: TokenHash = self._token_hasher.hash(request.raw_token)
        verification_object: EmailVerification = await self._email_verification_gateway.by_token_hash(token_hash)
        found_user: User = await self._user_gateway.by_id(verification_object.user_id)
        self._user_service.verify_email(now, found_user, verification_object)
