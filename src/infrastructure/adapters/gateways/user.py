from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError
from domain import User
from domain.value_objects import Id, Email
from application.ports.mappers import UserMapper
from application.exceptions import UserAlreadyExistsError, UserNotFoundError
from application.query_params import UserListParams
from infrastructure.models import User as ORMUser

__all__ = ["SqlAlchemyUserCommandGateway", "SqlAlchemyUserQueryGateway"]


class SqlAlchemyUserCommandGateway:

    def __init__(self, session: AsyncSession, mapper: UserMapper):
        self._session: AsyncSession = session
        self._mapper: UserMapper = mapper
    
    async def add(self, user: User):
        try:
            orm_user: ORMUser = self._mapper.to_dto(user)
            self._session.add(orm_user)
            await self._session.flush()
        except IntegrityError as e:
            await self._session.rollback()
            if getattr(e.orig, "sqlstate", None) == UniqueViolationError.sqlstate:
                raise UserAlreadyExistsError("User with same contacts already exists")
            raise

    async def delete(self, user: User): ...


class SqlAlchemyUserQueryGateway:

    def __init__(self, session: AsyncSession, mapper: UserMapper):
        self._session: AsyncSession = session
        self._mapper: UserMapper = mapper

    async def read_all(self, params: UserListParams) -> Sequence[User] | None:
        return None

    async def by_id(self, user_id: Id) -> User:
        stmt = select(ORMUser).where(ORMUser.id_ == user_id)
        response = await self._session.execute(stmt)
        user = response.scalar_one_or_none()

        if not user:
            raise UserNotFoundError("User with given id does not exist")
        return self._mapper.to_domain(user)

    async def by_email(self, user_email: Email) -> User:
        stmt = select(ORMUser).where(ORMUser.email == user_email)
        response = await self._session.execute(stmt)
        user = response.scalar_one_or_none()

        if not user:
            raise UserNotFoundError("User with given email does not exist")
        return self._mapper.to_domain(user)
