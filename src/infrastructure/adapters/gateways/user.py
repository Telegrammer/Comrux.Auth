from infrastructure.models import User as ORMUser
from domain import User
from setup import db_helper
from infrastructure.adapters.mappers import to_dto_mapper
from sqlalchemy.ext.asyncio import AsyncSession

__all__ = ["SqlAlchemyUserCommandGateway"]

class SqlAlchemyUserCommandGateway:

    async def add(self, user: User):
        session: AsyncSession = db_helper.session_getter()
        orm_user: ORMUser = to_dto_mapper.to(ORMUser).map(user)
        session.add(orm_user)
        await session.commit()
        await session.refresh(orm_user)

    async def delete(self, user: User):
        ...

