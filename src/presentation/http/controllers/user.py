from fastapi import APIRouter, HTTPException, Depends
from fastapi_error_map import ErrorAwareRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dishka.integrations.fastapi import FromDishka, inject
from starlette import status

from domain.exceptions import DomainFieldError
from application.ports import UnitOfWork, UserQueryGateway
from application.usecases.register_user import RegisterUserRequest, RegisterUserUsecase

from presentation.handlers import LoginHandler, RefreshHandler, JwtAuthInfoPresenter
from presentation.models import (
    UserCreate,
    UserLogin,
    UserRead,
    JwtInfo,
    SessionInfo,
    AuthInfo,
)

import jwt
from setup import settings

user_router = APIRouter(prefix="/user", tags=["user"])

http_bearer = HTTPBearer()


def create_register_user_router() -> APIRouter:

    router = ErrorAwareRouter()

    @router.post(
        "/register",
        error_map={DomainFieldError: status.HTTP_400_BAD_REQUEST},
        response_model=None,
    )
    @inject
    async def register(
        request_body: UserCreate,
        unit_of_work: FromDishka[UnitOfWork],
        interactor: FromDishka[RegisterUserUsecase],
    ):
        async with unit_of_work:
            await interactor(
                RegisterUserRequest.from_primitives(**request_body.model_dump())
            )

    return router


@user_router.post("/login", response_model=JwtInfo | SessionInfo)
@inject
async def login(request_body: UserLogin, handler: FromDishka[LoginHandler]):
    response: JwtInfo | SessionInfo | None = await handler(request_body)

    if response:
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )


@user_router.get("/refresh", response_model=JwtInfo)
@inject
async def refresh_token(
    jwt_presenter: FromDishka[JwtAuthInfoPresenter],
    refresh_handler: FromDishka[RefreshHandler],
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
):

    auth_info: AuthInfo | None = jwt_presenter.to_auth_info(
        token.credentials, "refresh"
    )
    if not auth_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    new_jwt_info: JwtInfo = await refresh_handler(auth_info)
    return new_jwt_info


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
