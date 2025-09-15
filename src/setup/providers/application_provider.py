from dishka import Provider, provide, Scope, from_context
from functools import partial
from typing import Callable
from setup.config import Settings
from domain import UserId
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
    LogoutUsecase,
    LogoutAllUsecase,
    BasicChangePasswordUsecase
)
from application.services import (
    CurrentUserService,
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
    user_id = from_context(UserId)

    timestamp_clock = provide(source=TimestampClock, provides=Clock)

    user_mapper = provide(source=SqlAlchemyUserMapper, provides=UserMapper)
    access_key_mapper = provide(source=RedisAccessKeyMapper, provides=AccessKeyMapper)

    @provide
    def provide_access_key_gateway_client(self, client: Redis) -> RedisAdapter:
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
    logout_user = provide(LogoutUsecase)
    logout_all = provide(LogoutAllUsecase)
    
    @provide
    def provide_current_user_service(
        self,
        gateway: UserQueryGateway,
        user_id: UserId,  
    ) -> CurrentUserService:
        return CurrentUserService(user_gateway=gateway, user_id=user_id)
    
    change_password = provide(BasicChangePasswordUsecase)
