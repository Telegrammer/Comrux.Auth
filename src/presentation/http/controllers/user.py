from fastapi import APIRouter, HTTPException
from dishka.integrations.fastapi import FromDishka, inject
from starlette.status import HTTP_401_UNAUTHORIZED

from domain import User

from application import RegisterUserUsecase, LoginUsecase

from infrastructure.models import User
from infrastructure.adapters import to_dto_mapper

from presentation.models import UserCreate, UserRead, UserLogin

__all__ = ["register", "login"]

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register")
@inject
async def register(
    request_body: UserCreate,
    interactor: FromDishka[RegisterUserUsecase]
):
    await interactor(**request_body.model_dump())
    


@router.post(
    "/login",
    response_model=UserRead
)
@inject
async def login(
    request_body: UserLogin,
    interactor: FromDishka[LoginUsecase]
):
    user: User | None = await interactor(**request_body.model_dump())
    
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not found")
    return to_dto_mapper.to(UserRead).map(user)