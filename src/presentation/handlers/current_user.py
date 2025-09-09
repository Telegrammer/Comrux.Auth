__all__ = ["CurrentUserHandler"]

from application.usecases.get_current_user import (
    GetCurrentUserRequest,
    GetCurrentUserUsecase,
    GetCurrentUserResponse,
)

from presentation.models import UserRead, AuthInfo


class CurrentUserHandler:

    def __init__(self, usecase: GetCurrentUserUsecase):
        self._usecase = usecase

    async def __call__(self, request: AuthInfo) -> UserRead:

        response: GetCurrentUserResponse = await self._usecase(
            GetCurrentUserRequest.from_primitives(**request.model_dump())
        )

        return UserRead(**response)
