from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dishka.integrations.fastapi import FromDishka, inject
from starlette.status import HTTP_401_UNAUTHORIZED

from application.ports import UnitOfWork
from application.usecases.register_user import RegisterUserRequest, RegisterUserUsecase

from presentation.handlers import LoginHandler
from presentation.models import UserCreate, UserLogin, UserRead, JwtInfo, SessionInfo

import jwt
from setup import settings

router = APIRouter(prefix="/user", tags=["user"])

http_bearer = HTTPBearer()

@router.post("/register")
@inject
async def register(
    request_body: UserCreate,
    unit_of_work: FromDishka[UnitOfWork],
    interactor: FromDishka[RegisterUserUsecase]
):  
    async with unit_of_work:
        await interactor(RegisterUserRequest.from_primitives(**request_body.model_dump()))

    


@router.post(
    "/login",
    response_model=JwtInfo | SessionInfo
)
@inject
async def login(
    request_body: UserLogin,
    handler: FromDishka[LoginHandler]
):
    response: JwtInfo | SessionInfo | None = await handler(request_body)

    if response:
        return response
    else: raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not found")



@router.get(
    "/me",
    response_model=UserRead
)
async def current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    
    response = jwt.decode(
        jwt=credentials.credentials,
        key=settings.auth.public_key.read_text(),
        algorithms=settings.auth.algorithm
    )
    return UserRead(user_id=response["sub"], phone=response["phone"], email=response["email"])