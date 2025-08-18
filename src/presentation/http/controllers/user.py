from fastapi import APIRouter, HTTPException
from dishka.integrations.fastapi import FromDishka, inject
from starlette.status import HTTP_401_UNAUTHORIZED

from application.ports import UnitOfWork
from application.usecases.register_user import RegisterUserRequest, RegisterUserUsecase
from application.usecases.login_user import LoginUserRequest, LoginUserResponse, LoginUsecase

from presentation.models import UserCreate, UserRead, UserLogin

__all__ = ["register", "login"]

router = APIRouter(prefix="/user", tags=["user"])


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
    response_model=UserRead
)
@inject
async def login(
    request_body: UserLogin,
    interactor: FromDishka[LoginUsecase]
):
    response: LoginUserResponse | None = await interactor(LoginUserRequest.from_primitives(**request_body.model_dump()))
    
    if not response:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not found")

    return UserRead(**response)