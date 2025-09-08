__all__ = ["StatefullLoginUsecase"]


from domain import AccessKey
from .contract import LoginUsecase, LoginMethod, LoginUserRequest, LoginUserResponse
from application.ports import AccessKeyCommandGateway


class StatefullLoginUsecase(LoginUsecase):

    def __init__(
        self, login_method: LoginMethod, access_key_gateway: AccessKeyCommandGateway
    ):
        super().__init__(login_method)
        self._access_key_gateway = access_key_gateway

    async def __call__(self, request: LoginUserRequest) -> LoginUserResponse:
        savable_key: AccessKey = await self._core(request)
        await self._access_key_gateway.add(savable_key)

        return LoginUserResponse.from_entity(savable_key)
