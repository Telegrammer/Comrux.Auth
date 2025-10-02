from datetime import timedelta
from dishka import Provider, provide, Scope, from_context
from setup.config import Settings
from domain.services import (
    UserService,
    EmailService,
    EmailVerificationService,
    AccessKeyService,
)
from domain.ports import (
    PasswordHasher,
    UserIdGenerator,
    AccessKeyIdGenerator,
    EmailIdGenerator,
    EmailVerificationTokenGenerator,
    EmailVerificationTokenHasher,
    EmailVerificationIdGenerator,
)
from domain.policies import AccessKeyValidityPolicy, EmailVerificationPolicy
from infrastructure.adapters.bcrypt_hasher import BcryptPasswordHasher
from infrastructure.adapters.user_uuid4_generator import UserUuid4Generator
from infrastructure.adapters.access_key_uuid4_generator import AccessKeyUuid4Generator
from infrastructure.adapters.email_uuid4_generator import EmailUuid4Generator
from infrastructure.adapters import (
    BcryptEmailVerificationTokenHasher,
    UrlsafeEmailVerificationTokenGenerator,
    Uuid7EmailVerificationIdGenerator,
)


class DomainProvider(Provider):
    scope = Scope.REQUEST

    settings = from_context(Settings, scope=Scope.APP)

    email_verification_token_hasher = provide(
        source=BcryptEmailVerificationTokenHasher, provides=EmailVerificationTokenHasher
    )
    email_verification_token_generator = provide(
        source=UrlsafeEmailVerificationTokenGenerator,
        provides=EmailVerificationTokenGenerator,
    )
    email_verification_id_generator = provide(
        source=Uuid7EmailVerificationIdGenerator,
        provides=EmailVerificationIdGenerator,
    )

    @provide(scope=Scope.APP)
    def provide_email_verification_policy(self) -> EmailVerificationPolicy:
        return EmailVerificationPolicy(
            token_ttl=timedelta(minutes=45), min_freshness_precentage=0.05
        )

    email_verification_service = provide(EmailVerificationService)
    email_id_generator = provide(source=EmailUuid4Generator, provides=EmailIdGenerator)
    password_hasher = provide(source=BcryptPasswordHasher, provides=PasswordHasher)
    user_id_generator = provide(source=UserUuid4Generator, provides=UserIdGenerator)
    email_service = provide(EmailService)
    user_service = provide(UserService)

    access_key_id_generator = provide(
        source=AccessKeyUuid4Generator, provides=AccessKeyIdGenerator
    )

    @provide(scope=Scope.APP)
    def provide_access_key_validity_policy(self) -> AccessKeyValidityPolicy:
        return AccessKeyValidityPolicy(
            ttl=timedelta(days=7), min_freshness_precentage=0.05
        )

    access_key_service = provide(AccessKeyService)
