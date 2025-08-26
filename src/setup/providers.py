__all__ = [
    "SettingsProvider",
    "DatabaseProvider",
    "DomainProvider",
    "ApplicationProvider",
    "PresentationProvider",
]

from typing import AsyncGenerator
from datetime import timedelta
from dishka import Provider, provide, Scope, from_context
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import MetaData
from setup.db_helper import DatabaseHelper
from setup.config import Settings

from domain import UserService, AccessKeyService
from domain.ports import PasswordHasher, UserIdGenerator, AccessKeyIdGenerator
from domain.policies import AccessKeyValidityPolicy

from application.ports import (
    UserCommandGateway,
    UserQueryGateway,
    UnitOfWork,
    UserMapper,
    Clock,
)
from application import (
    RegisterUserUsecase,
    PasswordLoginUsecase,
    RefreshUsecase,
    RefreshRequest,
    StatelessRefreshUsecase,
    StatelessRefreshRequest,
)

from infrastructure.adapters.bcrypt_hasher import BcryptPasswordHasher
from infrastructure.adapters.user_uuid4_generator import UserUuid4Generator
from infrastructure.adapters.sqlalchemy_unit_of_work import SqlAlchemyUnitOfWork
from infrastructure.adapters.timestamp_clock import TimestampClock
from infrastructure.adapters.access_key_uuid4_generator import AccessKeyUuid4Generator
from infrastructure.adapters.mappers.user import SqlAlchemyUserMapper

from infrastructure.adapters.gateways import (
    SqlAlchemyUserCommandGateway,
    SqlAlchemyUserQueryGateway,
)

from presentation.handlers import JwtAuthInfoPresenter, AuthInfoPresenter, LoginHandler, RefreshHandler
from presentation.models import JwtInfo, AuthInfo


class SettingsProvider(Provider):
    scope = Scope.APP

    @provide
    def get_settings(self) -> Settings:
        return Settings()


class DatabaseProvider(Provider):

    scope = Scope.APP
    settings = from_context(Settings)

    @provide
    def provide_db(self, settings: Settings) -> DatabaseHelper:
        return DatabaseHelper(
            url=str(settings.db.url),
            echo=settings.db.echo,
            echo_pool=settings.db.echo_pool,
            pool_size=settings.db.pool_size,
            max_overflow=settings.db.max_overflow,
        )

    @provide(scope=Scope.REQUEST)
    async def provide_session(
        self, db_helper: DatabaseHelper
    ) -> AsyncGenerator[AsyncSession, None]:
        async with db_helper.session_factory() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def provide_unit_of_work(
        self, session: AsyncSession
    ) -> AsyncGenerator[UnitOfWork, None]:
        async with SqlAlchemyUnitOfWork(session) as unit_of_work:
            yield unit_of_work


class DomainProvider(Provider):
    scope = Scope.REQUEST

    settings = from_context(Settings, scope=Scope.APP)

    password_hasher = provide(source=BcryptPasswordHasher, provides=PasswordHasher)
    user_id_generator = provide(source=UserUuid4Generator, provides=UserIdGenerator)
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
    


class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    settings = from_context(Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def provide_base_model_metadata(self, settings: Settings) -> MetaData:
        return MetaData(naming_convention=settings.db.naming_convention)

    timestamp_clock = provide(source=TimestampClock, provides=Clock)

    user_mapper = provide(source=SqlAlchemyUserMapper, provides=UserMapper)

    user_command_gateway = provide(
        source=SqlAlchemyUserCommandGateway, provides=UserCommandGateway
    )
    user_query_gateway = provide(
        source=SqlAlchemyUserQueryGateway, provides=UserQueryGateway
    )

    register_user = provide(RegisterUserUsecase)
    login_user = provide(PasswordLoginUsecase)
    refresh = provide(source=StatelessRefreshUsecase, provides=RefreshUsecase)


class PresentationProvider(Provider):
    scope = Scope.REQUEST

    settings = from_context(Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def provide_auth_info_presentation(self, settings: Settings) -> AuthInfoPresenter:
        return JwtAuthInfoPresenter(
            secret_key=settings.auth.secret_key.read_text(),
            public_key=settings.auth.public_key.read_text(),
            algorithm=settings.auth.algorithm,
            access_token_expiration_time=timedelta(
                minutes=settings.auth.access_token_expire_minutes
            ),
        )
    
    @provide(scope=Scope.APP)
    def provide_jwt_presentation(self, settings: Settings) -> JwtAuthInfoPresenter:
        return JwtAuthInfoPresenter(
            secret_key=settings.auth.secret_key.read_text(),
            public_key=settings.auth.public_key.read_text(),
            algorithm=settings.auth.algorithm,
            access_token_expiration_time=timedelta(
                minutes=settings.auth.access_token_expire_minutes
            ),
        )
    
    auth_info = provide(source=JwtInfo, provides=AuthInfo)
    
    login_handler = provide(LoginHandler)
    
    @provide
    @staticmethod
    def provide_refresh_handler(usecase: RefreshUsecase, presenter: AuthInfoPresenter) -> RefreshHandler:
        return RefreshHandler(
            StatelessRefreshRequest,
            usecase,
            presenter
        )

