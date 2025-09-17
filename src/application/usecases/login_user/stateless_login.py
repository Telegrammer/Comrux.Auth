__all__ = ["StatelessLoginUsecase"]


from domain import AccessKey
from .contract import LoginUsecase, LoginMethod, LoginUserRequest, LoginUserResponse


# In start of the making usecases, i thought that idea with single contract for all kind of type of usecase proparly working with OOP
#
class StatelessLoginUsecase(LoginUsecase):

    def __init__(self, login_method: LoginMethod):
        super().__init__(login_method)

    async def __call__(self, request: LoginUserRequest) -> LoginUserResponse:
        savable_key: AccessKey = await self._core(request)
        return LoginUserResponse.from_entity(savable_key)
