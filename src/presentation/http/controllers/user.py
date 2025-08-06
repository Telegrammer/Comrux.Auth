from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from domain import User
from infrastructure.models import User
from presentation.adapters import UserCreate, UserRead, UserLogin
from infrastructure.adapters import to_dto_mapper
from setup import db_helper
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends



from domain.services import UserService
from application import RegisterUserUsecase, LoginUsecase
from infrastructure.adapters import BcryptPasswordHasher, UserUuid4Generator, SqlAlchemyUserCommandGateway, SqlAlchemyUserQueryGateway

__all__ = ["register", "login"]

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register")
async def register(
    request_body: UserCreate,
):
    use_case = RegisterUserUsecase(
        UserService(BcryptPasswordHasher(), UserUuid4Generator()),
        SqlAlchemyUserCommandGateway()
    )
    await use_case(**request_body.model_dump())
    


@router.post(
    "/login",
    response_model=UserRead
)
async def login(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    request_body: UserLogin
):
    usecase = LoginUsecase(
        UserService(BcryptPasswordHasher(), UserUuid4Generator()),
        SqlAlchemyUserQueryGateway(session)
    )
    user: User | None = await usecase(**request_body.model_dump())
    
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not found")
    return to_dto_mapper.to(UserRead).map(user)