__all__ = ["LogoutAllUsecase"]


from domain import User

from application.ports import AccessKeyCommandGateway
from application.services import CurrentUserService

class LogoutAllUsecase:

    def __init__(
        self,
        current_user_service: CurrentUserService,
        access_key_gateway: AccessKeyCommandGateway,
    ):
        self._current_user_service: CurrentUserService = current_user_service
        self._access_key_gateway: AccessKeyCommandGateway = access_key_gateway

    async def __call__(self):
        current_user: User = await self._current_user_service()
        await self._access_key_gateway.delete_keys_by_user_id(current_user.id_)
