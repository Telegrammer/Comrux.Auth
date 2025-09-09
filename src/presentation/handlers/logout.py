__all__ = ["LogoutHandler"]


from application.ports import UnitOfWork
from application import LogoutUsecase, LogoutUserRequest


from presentation.models import AuthInfo


class LogoutHandler:

    def __init__(self, usecase: LogoutUsecase, unit_of_work: UnitOfWork):
        self._usecase = usecase
        self._unit_of_work = unit_of_work

    async def __call__(self, requset: AuthInfo):

        async with self._unit_of_work:
            await self._usecase(
                LogoutUserRequest.from_primitives(**requset.model_dump())
            )
