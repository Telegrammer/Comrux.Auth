from datetime import timedelta
from typing import Type
from dishka import Provider, provide, Scope, from_context, AsyncContainer
from setup.config import Settings
from presentation.handlers.adapters import (
    RefreshTokenBuilder,
    StatefullRefreshTokenBuilder,
    JwtAuthInfoPresenter,
)
from presentation.handlers.ports import AuthInfoPresenter, LoginUsecaseFactory
from presentation.handlers import (
    LoginHandler,
    RefreshHandler,
    RegisterHandler,
    CurrentUserHandler,
    LogoutHandler,
    LogoutAllHandler
)
from presentation.models import JwtInfo, AuthInfo, UserLogin, PasswordUserLogin
from application import (
    RefreshUsecase,
    StatefullRefreshRequest,
    LoginMethod,
    PasswordLoginMethod,
    LoginUserRequest,
    PasswordLoginUserRequest,
)


class PresentationProvider(Provider):
    scope = Scope.REQUEST

    settings = from_context(Settings, scope=Scope.APP)
    token_builder = provide(
        source=StatefullRefreshTokenBuilder,
        provides=RefreshTokenBuilder,
        scope=Scope.APP,
    )

    @provide(scope=Scope.APP)
    def provide_jwt_presentation(
        self, settings: Settings, token_builder: RefreshTokenBuilder
    ) -> JwtAuthInfoPresenter:
        return JwtAuthInfoPresenter(
            secret_key=settings.auth.secret_key.read_text(),
            public_key=settings.auth.public_key.read_text(),
            algorithm=settings.auth.algorithm,
            access_token_expiration_time=timedelta(
                minutes=settings.auth.access_token_expire_minutes
            ),
            token_builder=token_builder,
        )

    @provide(scope=Scope.APP)
    def provide_auth_info_presentation(
        self, presenter: JwtAuthInfoPresenter
    ) -> AuthInfoPresenter:
        return presenter

    auth_info = provide(source=JwtInfo, provides=AuthInfo)

    register_handler = provide(source=RegisterHandler)

    @provide
    async def provide_login_methods(
        self, container: AsyncContainer
    ) -> dict[Type[UserLogin], tuple[LoginMethod, Type[LoginUserRequest]]]:
        return {
            PasswordUserLogin: (
                await container.get(PasswordLoginMethod),
                PasswordLoginUserRequest,
            ),
        }

    login_factory = provide(LoginUsecaseFactory)
    login_handler = provide(LoginHandler)

    @provide
    def provide_refresh_handler(
        self, usecase: RefreshUsecase, presenter: AuthInfoPresenter
    ) -> RefreshHandler:
        return RefreshHandler(StatefullRefreshRequest, usecase, presenter)

    current_user_handler = provide(CurrentUserHandler)
    logout_user_handler = provide(LogoutHandler)
    logout_all_handler = provide(LogoutAllHandler)
