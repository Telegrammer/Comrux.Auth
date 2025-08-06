from infrastructure.models import User as ORMUser
from domain import User
from setup import db_helper
from infrastructure.adapters.mappers import to_dto_mapper, to_domain
from sqlalchemy.ext.asyncio import AsyncSession
from application.ports.gateways import UserQueryGateway
from application.query_params import UserListParams
from typing import Sequence
from domain.value_objects import Id, Email
from sqlalchemy import select
from typing import Annotated
from fastapi import Depends

__all__ = ["SqlAlchemyUserCommandGateway", "SqlAlchemyUserQueryGateway"]

class SqlAlchemyUserCommandGateway:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, user: User):
        orm_user: ORMUser = to_dto_mapper.to(ORMUser).map(user)
        self._session.add(orm_user)
        await self._session.commit()
        await self._session.refresh(orm_user)

    async def delete(self, user: User):
        ...


class SqlAlchemyUserQueryGateway(UserQueryGateway):

    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def read_all(self, params: UserListParams) -> Sequence[User] | None:
        return None

    async def by_id(self, user_id: Id) -> User | None:
        stmt = select(ORMUser).where(ORMUser.id_ == user_id)
        response = await self._session.execute(stmt)
        user = response.scalar_one_or_none()
        return to_domain(user) if user else None
    
    async def by_email(self, user_email: Email) -> User | None:
        stmt = select(ORMUser).where(ORMUser.email == user_email)
        response = await self._session.execute(stmt)
        user = response.scalar_one_or_none()
        return to_domain(user, User) if user else None

    
