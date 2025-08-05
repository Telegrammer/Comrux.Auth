import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK

from domain import User as DomainUser
from domain.value_objects import Uuid4, Email, PhoneNumber, PasswordHash, RawPassword
from infrastructure.models import User
from setup import db_helper
from passlib.context import CryptContext
from presentation.adapters import UserCreate, UserRead
from infrastructure.adapters import to_dto_mapper



from domain.services import UserService
from application import RegisterUserUsecase
from infrastructure.adapters import BycryptPasswordHasher, UserUuid4Generator, SqlAlchemyUserCommandGateway

__all__ = ["create_user", "get_user"]

router = APIRouter(prefix="/users", tags=["user"])


@router.post("")
async def create_user(
    request_body: UserCreate,
):
    use_case = RegisterUserUsecase(
        UserService(BycryptPasswordHasher(), UserUuid4Generator()),
        SqlAlchemyUserCommandGateway()
    )
    use_case(**request_body.model_dump())
    


@router.get(
    "/{user_id}",
    response_model=UserRead,
    responses={HTTP_404_NOT_FOUND: {}, HTTP_200_OK: {}},
)
async def get_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)], user_id: UUID4
):
    stmt = select(User).where(User.id_ == user_id)
    response = await session.execute(stmt)
    result = response.one_or_none()[0]

    domain_user = DomainUser(
        id_=Uuid4(value=str(result.id_)),
        email=Email(value=result.email),
        phone=PhoneNumber(value=result.phone),
        password_hash=PasswordHash(value=result.password_hash),
    )
    json_user = to_dto_mapper.to(UserRead).map(domain_user)

    if not result:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    else:
        return json_user
