from typing import AsyncGenerator
from dishka import Provider, provide, Scope, from_context
from sqlalchemy.ext.asyncio import AsyncSession
from setup.db_helper import DatabaseHelper
from setup.config import Settings

from domain import UserService
from domain.ports import PasswordHasher, UserIdGenerator


from application.ports import UserCommandGateway, UserQueryGateway, UnitOfWork, UserMapper
from application import RegisterUserUsecase, LoginUsecase

from infrastructure.adapters.bcrypt_hasher import BcryptPasswordHasher
from infrastructure.adapters.user_uuid4_generator import UserUuid4Generator
from infrastructure.adapters.sqlalchemy_unit_of_work import SqlAlchemyUnitOfWork
from infrastructure.adapters.mappers.user import SqlAlchemyUserMapper

from infrastructure.adapters.gateways import (
    SqlAlchemyUserCommandGateway,
    SqlAlchemyUserQueryGateway,
)


__all__ = ["DatabaseProvider", "UsecaseProvider"]


class DatabaseProvider(Provider):

    scope = Scope.APP
    settings = from_context(provides=Settings)

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

    password_hasher = provide(source=BcryptPasswordHasher, provides=PasswordHasher)
    user_id_generator = provide(source=UserUuid4Generator, provides=UserIdGenerator)
    user_service = provide(UserService)

class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    user_mapper = provide(source=SqlAlchemyUserMapper, provides=UserMapper)
    
    user_command_gateway = provide(
        source=SqlAlchemyUserCommandGateway, provides=UserCommandGateway
    )
    user_query_gateway = provide(
        source=SqlAlchemyUserQueryGateway, provides=UserQueryGateway
    )

    register_user = provide(RegisterUserUsecase)
    login_user = provide(LoginUsecase)