from application.ports import UnitOfWork
from application.exceptions import UserAlreadyExistsError
from sqlalchemy.ext.asyncio import AsyncSession

__all__ = ["SqlAlchemyUnitOfWork"]


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self._session.commit()
        else:
            await self._session.rollback()

        
