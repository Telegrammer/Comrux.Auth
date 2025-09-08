from fastapi import APIRouter, HTTPException, Depends
from fastapi_error_map import ErrorAwareRouter, rule
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dishka.integrations.fastapi import FromDishka, inject
from starlette import status

from domain.exceptions import DomainFieldError
from application.ports import UnitOfWork, UserQueryGateway
from application.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    UserAuthenticationError,
    ExpiredAccessKeyError,
    AccessKeyNotFound,
)
from application.ports.mappers.errors import MappingError
from application.ports.gateways.errors import GatewayFailedError

from presentation.handlers import (
    LoginHandler,
    RefreshHandler,
    JwtAuthInfoPresenter,
    RegisterHandler,
)
from presentation.models import (
    UserCreate,
    PasswordUserLogin,
    UserRead,
    JwtInfo,
    SessionInfo,
    AuthInfo,
)

from presentation.exceptions import (
    InvalidTokenTypeError,
)

import jwt
from setup import settings

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
            GatewayFailedError: status.HTTP_503_SERVICE_UNAVAILABLE
        },
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


@user_router.get(
    "/me",
)
@inject
async def current_user(
    unit_of_work: FromDishka[UnitOfWork],
    gateway: FromDishka[UserQueryGateway],
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
):

    response = jwt.decode(
        jwt=token.credentials,
        key=settings.auth.public_key.read_text(),
        algorithms=settings.auth.algorithm,
    )

    async with unit_of_work:

        user = await gateway.by_id(response["user_id"])

        return UserRead(email=user.email, phone=user.phone, user_id=user.id_)


user_router.include_router(create_register_user_router())

user_router.include_router(create_login_router())

user_router.include_router(create_refresh_router())
