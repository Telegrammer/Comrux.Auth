__all__ = ["StatelessLoginUsecase"]


from domain import AccessKey
from .contract import LoginUsecase, LoginMethod, LoginUserRequest, LoginUserResponse


# In start of the making usecases,
# i thought that idea with single contract for all kind of type of usecase works proparly with OOP polymorph concept
# but i realized, if i had this realization in languages with static typing (C#, Java, C++), then usecase must provide downcast to ancestors of request type
# this kind of operation brings new unpredictable runtime-errors, which i don't want to met them even when i coding on Python
# so i must refactor usecases with that kind of requests
class StatelessLoginUsecase[reqT: LoginUserRequest](LoginUsecase):

    def __init__(self, login_method: LoginMethod[reqT]):
        super().__init__(login_method)

    async def __call__(self, request: reqT) -> LoginUserResponse:
        savable_key: AccessKey = await self._core(request)
        return LoginUserResponse.from_entity(savable_key)
