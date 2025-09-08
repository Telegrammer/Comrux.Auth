from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import MetaData
from redis.asyncio import Redis, from_url
from dishka import Provider, provide, Scope, from_context
from setup.db_helper import DatabaseHelper
from setup.config import Settings
from application.ports import UnitOfWork
from infrastructure.adapters.sqlalchemy_transaction import SqlAlchemyTransaction
from infrastructure.adapters.redis_transaction import RedisTransaction


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
