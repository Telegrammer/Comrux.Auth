from fastapi import APIRouter, HTTPException
from dishka.integrations.fastapi import FromDishka, inject
from starlette.status import HTTP_401_UNAUTHORIZED

from application.ports import UnitOfWork
from application.usecases.register_user import RegisterUserRequest, RegisterUserUsecase

<<<<<<< HEAD
from application.usecases.register_user import RegisterUserRequest, RegisterUserUsecase
from application.usecases.login_user import LoginUserRequest, LoginUserResponse, LoginUsecase

from presentation.models import UserCreate, UserRead, UserLogin
=======
from presentation.handlers import LoginHandler
from presentation.models import UserCreate, UserLogin, JwtInfo
>>>>>>> dev

__all__ = ["register", "login"]

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register")
@inject
async def register(
    request_body: UserCreate,
    unit_of_work: FromDishka[UnitOfWork],
    interactor: FromDishka[RegisterUserUsecase]
<<<<<<< HEAD
):
    await interactor(RegisterUserRequest.from_primitives(**request_body.model_dump()))
=======
):  
    async with unit_of_work:
        await interactor(RegisterUserRequest.from_primitives(**request_body.model_dump()))

>>>>>>> dev
    


@router.post(
    "/login",
    response_model=JwtInfo
)
@inject
async def login(
    request_body: UserLogin,
    handler: FromDishka[LoginHandler]
):
<<<<<<< HEAD
    response: LoginUserResponse | None = await interactor(LoginUserRequest.from_primitives(**request_body.model_dump()))
    
    if not response:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not found")

    return UserRead(**response)
=======
    response: JwtInfo | None = await handler(request_body)

    if response:
        return response
    else: raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not found")
>>>>>>> dev
