__all__ = ["RegisterHandler"]

from application.usecases.register_user import (
    RegisterUserRequest,
    RegisterUserUsecase,
)

from application.ports import UnitOfWork
from presentation.models import UserCreate


class RegisterHandler:

    def __init__(self, register_usecase: RegisterUserUsecase, unit_of_work: UnitOfWork):
        self._register_usecase = register_usecase
        self._unit_of_work = unit_of_work

    async def __call__(self, request: UserCreate) -> None:
        async with self._unit_of_work:
            await self._register_usecase(
                RegisterUserRequest.from_primitives(**request.model_dump())
            )
