__all__ = ["StatelessLoginUsecase"]


from domain import AccessKey
from .contract import LoginUsecase, LoginMethod, LoginUserRequest, LoginUserResponse


class StatelessLoginUsecase[reqT: LoginUserRequest](LoginUsecase):

    def __init__(self, login_method: LoginMethod[reqT]):
        super().__init__(login_method)

    async def __call__(self, request: reqT) -> LoginUserResponse:
        savable_key: AccessKey = await self._core(request)
        return LoginUserResponse.from_entity(savable_key)
