__all__ = ["SqlAlchemyTransaction"]


from sqlalchemy.ext.asyncio import AsyncSession


from application.ports import Transaction


class SqlAlchemyTransaction(Transaction):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def complete(self) -> None:
        await self._session.commit()

    async def cancel(self):
        await self._session.rollback()