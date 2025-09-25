from typing import Sequence


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError


from domain import User, UserId
from domain.value_objects import Email

from application.query_params import UserListParams
from application.ports.mappers import UserMapper
from application.exceptions import UserAlreadyExistsError, UserNotFoundError
from application.ports.gateways.errors import GatewayFailedError
from infrastructure.models import User as ORMUser
from infrastructure.exceptions.common import create_error_aware_decorator


network_error_aware = create_error_aware_decorator(
    {frozenset({ConnectionRefusedError, ConnectionResetError}): GatewayFailedError}
)

from application.ports.gateways.errors import GatewayFailedError

__all__ = ["SqlAlchemyUserCommandGateway", "SqlAlchemyUserQueryGateway"]


class SqlAlchemyUserCommandGateway:

    def __init__(self, session: AsyncSession, mapper: UserMapper):
        self._session: AsyncSession = session
        self._mapper: UserMapper = mapper

    @network_error_aware("Cannot add user: users are not reachable")
    async def add(self, user: User):
        try:
            orm_user: ORMUser = self._mapper.to_dto(user)
            self._session.add(orm_user)
            await self._session.flush()
        except IntegrityError as e:
            original_error = e.orig
            if (
                getattr(original_error, "sqlstate", None)
                != UniqueViolationError.sqlstate
            ):
                raise

            error_detail: str = str(original_error).split("\n")[1]
            if error_detail.startswith("DETAIL:  Key (id_)"):
                raise GatewayFailedError(
                    "Somehow user created with the same id. Please try again"
                )

            raise UserAlreadyExistsError("User with same data already exists")

    @network_error_aware("Cannot delete user: we don't know where are the users")
    async def delete(self, user: User) -> None:
        orm_user = self._mapper.to_dto(user)
        await self._session.delete(orm_user)
    
    async def update(self, user: User) -> None:
        orm_user = self._mapper.to_dto(user)
        await self._session.merge(orm_user)



class SqlAlchemyUserQueryGateway:

    def __init__(self, session: AsyncSession, mapper: UserMapper):
        self._session: AsyncSession = session
        self._mapper: UserMapper = mapper

    async def read_all(self, params: UserListParams) -> Sequence[User] | None:
        return None

    @network_error_aware("Cannot find user: can't reach to them")
    async def by_id(self, user_id: UserId) -> User:
        stmt = select(ORMUser).where(ORMUser.id_ == user_id)
        response = await self._session.execute(stmt)
        user = response.scalar_one_or_none()

        if not user:
            raise UserNotFoundError("User with given id does not exist")
        return self._mapper.to_domain(user)

    @network_error_aware("Cannot find user: can't reach to them")
    async def by_email(self, user_email: Email) -> User:
        stmt = select(ORMUser).where(ORMUser.email == user_email)
        response = await self._session.execute(stmt)
        user = response.scalar_one_or_none()

        if not user:
            raise UserNotFoundError("User with given email does not exist")
        return self._mapper.to_domain(user)
