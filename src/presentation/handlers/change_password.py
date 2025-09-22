__all__ = ["ChangePasswordHandler"]


from application import (
    BasicChangePasswordRequest,
    BasicChangePasswordUsecase,
)

from application.ports import UnitOfWork
from presentation.models import PasswordChange

#TODO: replace logic with unit of work into application composition layer
# also it would be more understandable if we keep usecase call (maybe somehow we could hide composition logic)
class ChangePasswordHandler:

    def __init__(
        self,
        change_password_usecase: BasicChangePasswordUsecase,
        unit_of_work: UnitOfWork,
    ):
        self._change_password_usecase: BasicChangePasswordUsecase = (
            change_password_usecase
        )
        self._unit_of_work: UnitOfWork = unit_of_work

    async def __call__(self, request: PasswordChange, logout_all: bool):

        async with self._unit_of_work:
            await self._change_password_usecase(
                BasicChangePasswordRequest.from_primitives(
                    **{**request.model_dump(), "logout_all": logout_all}
                )
            )
