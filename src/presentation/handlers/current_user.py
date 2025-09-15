__all__ = ["CurrentUserHandler"]

from application.usecases.get_current_user import (
    GetCurrentUserUsecase,
    GetCurrentUserResponse,
)

from presentation.models import UserRead


class CurrentUserHandler:

    def __init__(self, usecase: GetCurrentUserUsecase):
        self._usecase = usecase

    async def __call__(self) -> UserRead:

        response: GetCurrentUserResponse = await self._usecase()
        return UserRead(**response)
