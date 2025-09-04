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
from redis.asyncio import Redis, from_url
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
    AccessKeyCommandGateway,
    AccessKeyQueryGateway,
    AccessKeyMapper
)
from application import (
    RegisterUserUsecase,
    PasswordLoginUsecase,
    RefreshUsecase,
    StatefullRefreshUsecase,
    StatefullRefreshRequest,
)

from infrastructure.adapters.bcrypt_hasher import BcryptPasswordHasher
from infrastructure.adapters.user_uuid4_generator import UserUuid4Generator
from infrastructure.adapters.timestamp_clock import TimestampClock
from infrastructure.adapters.access_key_uuid4_generator import AccessKeyUuid4Generator
from infrastructure.adapters.mappers.user import SqlAlchemyUserMapper
from infrastructure.adapters.mappers.access_key import RedisAccessKeyMapper
from infrastructure.adapters.sqlalchemy_transaction import SqlAlchemyTransaction
from infrastructure.adapters.redis_transaction import RedisTransaction

from infrastructure.adapters.gateways import (
    SqlAlchemyUserCommandGateway,
    SqlAlchemyUserQueryGateway,
    RedisAccessKeyQueryGateway,
    RedisAccessKeyCommandGateway,
)

from presentation.handlers.adapters import (
    RefreshTokenBuilder,
    StatefullRefreshTokenBuilder,
    JwtAuthInfoPresenter,
)

from presentation.handlers.ports import (
    AuthInfoPresenter,
)

from presentation.handlers import (
    LoginHandler,
    RefreshHandler,
    RegisterHandler,
)

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
    
    @provide
    def provide_base_model_metadata(self, settings: Settings) -> MetaData:
        return MetaData(naming_convention=settings.db.naming_convention)

    unit_of_work = provide(UnitOfWork, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    async def provide_user_session(
        self, db_helper: DatabaseHelper, unit_of_work: UnitOfWork
    ) -> AsyncGenerator[AsyncSession, None]:
        async with db_helper.session_factory() as session:
            unit_of_work.add(SqlAlchemyTransaction(session))
            yield session

    @provide(scope=Scope.REQUEST)
    async def provide_access_key_client(
        self, settings: Settings, unit_of_work: UnitOfWork
    ) -> AsyncGenerator[Redis, None]:
        async with Redis.pipeline(
            from_url(str(settings.cache.url)), transaction=True
        ) as client:
            unit_of_work.add(RedisTransaction(client))
            yield client


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

    timestamp_clock = provide(source=TimestampClock, provides=Clock)

    user_mapper = provide(source=SqlAlchemyUserMapper, provides=UserMapper)
    access_key_mapper=provide(source=RedisAccessKeyMapper, provides=AccessKeyMapper)

    user_command_gateway = provide(
        source=SqlAlchemyUserCommandGateway, provides=UserCommandGateway
    )
    user_query_gateway = provide(
        source=SqlAlchemyUserQueryGateway, provides=UserQueryGateway
    )

    access_key_command_gateway = provide(
        source=RedisAccessKeyCommandGateway, provides=AccessKeyCommandGateway
    )
    access_key_query_gateway = provide(
        source=RedisAccessKeyQueryGateway, provides=AccessKeyQueryGateway
    )

    register_user = provide(RegisterUserUsecase)
    login_user = provide(PasswordLoginUsecase)
    refresh = provide(source=StatefullRefreshUsecase, provides=RefreshUsecase)


class PresentationProvider(Provider):
    scope = Scope.REQUEST

    settings = from_context(Settings, scope=Scope.APP)
    token_builder = provide(source=StatefullRefreshTokenBuilder, provides=RefreshTokenBuilder, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def provide_jwt_presentation(self, settings: Settings, token_builder: RefreshTokenBuilder) -> JwtAuthInfoPresenter:
        return JwtAuthInfoPresenter(
            secret_key=settings.auth.secret_key.read_text(),
            public_key=settings.auth.public_key.read_text(),
            algorithm=settings.auth.algorithm,
            access_token_expiration_time=timedelta(
                minutes=settings.auth.access_token_expire_minutes
            ),
            token_builder=token_builder
        )
    
    @provide(scope=Scope.APP)
    def provide_auth_info_presentation(self, presenter: JwtAuthInfoPresenter) -> AuthInfoPresenter:
        return presenter


    auth_info = provide(source=JwtInfo, provides=AuthInfo)

    register_handler = provide(source=RegisterHandler)
    login_handler = provide(LoginHandler)


    # I made this kind of realization with type of request instead of polymorph
    # because i don't want to create another nesting, like i did it earlier with usecases
    # TODO: it would be better to make it without pointing of request type
    @provide
    def provide_refresh_handler(
        self, usecase: RefreshUsecase, presenter: AuthInfoPresenter
    ) -> RefreshHandler:
        return RefreshHandler(StatefullRefreshRequest, usecase, presenter)
