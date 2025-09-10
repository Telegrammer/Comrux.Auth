__all__ = ["LogoutAllHandler"]


from application import LogoutAllUsecase, LogoutAllUserRequest
from application.ports import UnitOfWork
from presentation.models import AuthInfo


class LogoutAllHandler:

    def __init__(self, usecase: LogoutAllUsecase, unit_of_work: UnitOfWork):
        self._usecase = usecase
        self._unit_of_work = unit_of_work
    
    async def __call__(self, request: AuthInfo):
        async with self._unit_of_work:
            await self._usecase(LogoutAllUserRequest.from_primitives(**request.model_dump()))
