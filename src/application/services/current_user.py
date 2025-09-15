__all__ = ["CurrentUserService"]


from application.ports import UserQueryGateway


from domain import User, UserId


class CurrentUserService:

    def __init__(self, user_id: UserId, user_gateway: UserQueryGateway):
        self._user_id: UserId = user_id
        self._user_gateway: UserQueryGateway = user_gateway

    async def __call__(self) -> User:
        return await self._user_gateway.by_id(self._user_id.value)

    @property
    def user_id(self) -> UserId:
        return self._user_id
