from fastapi import APIRouter, Depends
from fastapi_error_map import ErrorAwareRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dishka.integrations.fastapi import FromDishka, inject
from starlette import status

from domain.exceptions import DomainFieldError
from application.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    UserAuthenticationError,
    ExpiredAccessKeyError,
    AccessKeyNotFound,
    WrongPasswordError,
)
from application.ports.mappers.errors import MappingError
from application.ports.gateways.errors import GatewayFailedError
from presentation.handlers import (
    LoginHandler,
    RefreshHandler,
    JwtAuthInfoPresenter,
    RegisterHandler,
    CurrentUserHandler,
    LogoutHandler,
    LogoutAllHandler,
    ChangePasswordHandler,
)
from presentation.models import (
    UserCreate,
    PasswordUserLogin,
    PasswordChange,
    UserRead,
    JwtInfo,
    SessionInfo,
    AuthInfo,
)

from presentation.constans import TokenType

from presentation.exceptions import (
    InvalidTokenTypeError,
)

user_router = APIRouter(prefix="/user", tags=["user"])

http_bearer = HTTPBearer()


def create_register_user_router() -> APIRouter:
    router = ErrorAwareRouter()

    @router.post(
        "/register",
        error_map={
            MappingError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            DomainFieldError: status.HTTP_400_BAD_REQUEST,
            UserAlreadyExistsError: status.HTTP_409_CONFLICT,
            GatewayFailedError: status.HTTP_503_SERVICE_UNAVAILABLE,
        },
        status_code=status.HTTP_201_CREATED,
        response_model=None,
    )
    @inject
    async def register(
        request_body: UserCreate,
        handler: FromDishka[RegisterHandler],
    ):
        await handler(request_body)

    return router


def create_login_router() -> APIRouter:
    router = ErrorAwareRouter()

    @router.post(
        "/login",
        error_map={
            MappingError: status.HTTP_500_INTERNAL_SERVER_ERROR,
            DomainFieldError: status.HTTP_400_BAD_REQUEST,
            UserNotFoundError: status.HTTP_404_NOT_FOUND,
            UserAuthenticationError: status.HTTP_401_UNAUTHORIZED,
        },
        response_model=JwtInfo | SessionInfo,
    )
    @inject
    async def login(request_body: PasswordUserLogin, handler: FromDishka[LoginHandler]):
        return await handler(request_body)

    return router


def create_refresh_router() -> APIRouter:
    router = ErrorAwareRouter()

    @router.get(
        "/refresh",
        error_map={
            InvalidTokenTypeError: status.HTTP_401_UNAUTHORIZED,
            DomainFieldError: status.HTTP_400_BAD_REQUEST,
            ExpiredAccessKeyError: status.HTTP_401_UNAUTHORIZED,
            AccessKeyNotFound: status.HTTP_401_UNAUTHORIZED,
            MappingError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
        response_model=JwtInfo,
    )
    @inject
    async def refresh_token(
        jwt_presenter: FromDishka[JwtAuthInfoPresenter],
        handler: FromDishka[RefreshHandler],
        token: HTTPAuthorizationCredentials = Depends(http_bearer),
    ):

        auth_info: AuthInfo = jwt_presenter.to_auth_info(token.credentials, "refresh")
        return await handler(auth_info)

    return router


def create_current_user_router():

    router = ErrorAwareRouter()

    @router.get(
        "/me",
        error_map={
            InvalidTokenTypeError: status.HTTP_401_UNAUTHORIZED,
            DomainFieldError: status.HTTP_400_BAD_REQUEST,
            ExpiredAccessKeyError: status.HTTP_401_UNAUTHORIZED,
            UserNotFoundError: status.HTTP_401_UNAUTHORIZED,
            GatewayFailedError: status.HTTP_503_SERVICE_UNAVAILABLE,
            MappingError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
        response_model=UserRead,
    )
    @inject
    async def current_user(
        handler: FromDishka[CurrentUserHandler],
        jwt_presenter: FromDishka[JwtAuthInfoPresenter],
        token: HTTPAuthorizationCredentials = Depends(http_bearer),
    ):

        jwt_presenter.to_auth_info(token.credentials, "access")
        return await handler()

    return router


def create_logout_router():

    router = ErrorAwareRouter()

    @router.delete(
        "/logout",
        error_map={
            DomainFieldError: status.HTTP_401_UNAUTHORIZED,
            GatewayFailedError: status.HTTP_503_SERVICE_UNAVAILABLE,
            AccessKeyNotFound: status.HTTP_401_UNAUTHORIZED,
        },
        status_code=status.HTTP_204_NO_CONTENT,
        response_model=None,
    )
    @inject
    async def logout(
        handler: FromDishka[LogoutHandler],
        jwt_presenter: FromDishka[JwtAuthInfoPresenter],
        token: HTTPAuthorizationCredentials = Depends(http_bearer),
    ):
        auth_info: AuthInfo = jwt_presenter.to_auth_info(token.credentials, "refresh")
        return await handler(auth_info)

    return router

def create_logout_all_router():

    router = ErrorAwareRouter()

    @router.delete(
        "/logout-all",
        error_map={
            DomainFieldError: status.HTTP_401_UNAUTHORIZED,
            GatewayFailedError: status.HTTP_503_SERVICE_UNAVAILABLE,
            AccessKeyNotFound: status.HTTP_401_UNAUTHORIZED,
        },
        status_code=status.HTTP_204_NO_CONTENT,
        response_model=None,
    )
    @inject
    async def logout_all(
        handler: FromDishka[LogoutAllHandler],
        jwt_presenter: FromDishka[JwtAuthInfoPresenter],
        token: HTTPAuthorizationCredentials = Depends(http_bearer),
    ):
        jwt_presenter.to_auth_info(token.credentials, "access")
        return await handler()

    return router


def create_change_password_router():
    router = ErrorAwareRouter()


    @router.patch(
        "/change-password",
        error_map={
            DomainFieldError: status.HTTP_400_BAD_REQUEST,
            GatewayFailedError: status.HTTP_503_SERVICE_UNAVAILABLE,
            AccessKeyNotFound: status.HTTP_401_UNAUTHORIZED,
            ExpiredAccessKeyError: status.HTTP_401_UNAUTHORIZED,
            InvalidTokenTypeError: status.HTTP_403_FORBIDDEN,
            WrongPasswordError: status.HTTP_403_FORBIDDEN,
        },
        status_code=status.HTTP_202_ACCEPTED,
        response_model=None
    )
    @inject
    async def change_password(
        request_body: PasswordChange,
        presenter: FromDishka[JwtAuthInfoPresenter],
        handler: FromDishka[ChangePasswordHandler],
        token: HTTPAuthorizationCredentials = Depends(http_bearer),
    ):  
        presenter.to_auth_info(token.credentials, TokenType.ACCESS)
        return await handler(request_body)
    return router



user_router.include_router(create_register_user_router())
user_router.include_router(create_login_router())
user_router.include_router(create_refresh_router())
user_router.include_router(create_current_user_router())
user_router.include_router(create_logout_router())
user_router.include_router(create_logout_all_router())
user_router.include_router(create_change_password_router())