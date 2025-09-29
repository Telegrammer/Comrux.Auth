from datetime import timedelta
from dishka import Provider, provide, Scope, from_context
from setup.config import Settings
from domain import UserService, AccessKeyService
from domain.services.email import EmailService
from domain.ports import PasswordHasher, UserIdGenerator, AccessKeyIdGenerator, EmailIdGenerator
from domain.policies import AccessKeyValidityPolicy
from infrastructure.adapters.bcrypt_hasher import BcryptPasswordHasher
from infrastructure.adapters.user_uuid4_generator import UserUuid4Generator
from infrastructure.adapters.access_key_uuid4_generator import AccessKeyUuid4Generator
from infrastructure.adapters.email_uuid4_generator import EmailUuid4Generator


class DomainProvider(Provider):
    scope = Scope.REQUEST

    settings = from_context(Settings, scope=Scope.APP)

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