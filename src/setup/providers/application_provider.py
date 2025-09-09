from dishka import Provider, provide, Scope, from_context
from functools import partial
from typing import Callable
from setup.config import Settings
from application.ports import (
    UserCommandGateway,
    UserQueryGateway,
    UserMapper,
    Clock,
    AccessKeyCommandGateway,
    AccessKeyQueryGateway,
    AccessKeyMapper,
)
from application import (
    RegisterUserUsecase,
    LoginUsecase,
    LoginMethod,
    PasswordLoginMethod,
    StatefullLoginUsecase,
    RefreshUsecase,
    StatefullRefreshUsecase,
    GetCurrentUserUsecase,
)
from infrastructure.adapters.timestamp_clock import TimestampClock
from infrastructure.adapters.mappers.user import SqlAlchemyUserMapper
from infrastructure.adapters.mappers.access_key import RedisAccessKeyMapper
from infrastructure.adapters.redis_adapter import RedisAdapter
from infrastructure.adapters.gateways import (
    SqlAlchemyUserCommandGateway,
    SqlAlchemyUserQueryGateway,
    RedisAccessKeyQueryGateway,
    RedisAccessKeyCommandGateway,
)
from redis.asyncio import Redis


class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    settings = from_context(Settings, scope=Scope.APP)

    timestamp_clock = provide(source=TimestampClock, provides=Clock)

    user_mapper = provide(source=SqlAlchemyUserMapper, provides=UserMapper)
    access_key_mapper = provide(source=RedisAccessKeyMapper, provides=AccessKeyMapper)

    @provide
    async def provide_access_key_gateway_client(self, client: Redis) -> RedisAdapter:
        return RedisAdapter(client)

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

    password_login_method = provide(PasswordLoginMethod)

    @provide
    def provide_login_usecase_constructor(
        self, gateway: AccessKeyCommandGateway
    ) -> Callable[[LoginMethod], LoginUsecase]:
        return partial(StatefullLoginUsecase, access_key_gateway=gateway)

    refresh = provide(source=StatefullRefreshUsecase, provides=RefreshUsecase)

    get_current_user = provide(GetCurrentUserUsecase)
