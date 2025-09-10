__all__ = ["LogoutAllUserRequest", "LogoutAllUsecase"]


from dataclasses import dataclass

from domain import AccessKeyId, AccessKey

from application.ports import AccessKeyCommandGateway, AccessKeyQueryGateway
from application.exceptions import AccessKeyNotFound

@dataclass
class LogoutAllUserRequest:

    access_key_id: AccessKeyId

    @classmethod
    def from_primitives(
        cls, *, key_id: str, **_
    ) -> "LogoutAllUserRequest":
        return cls(access_key_id=key_id)


class LogoutAllUsecase:


    def __init__(
        self,
        access_key_commands: AccessKeyCommandGateway,
        access_key_queries: AccessKeyQueryGateway,
    ):
        self._access_key_commands: AccessKeyCommandGateway = access_key_commands
        self._access_key_queries: AccessKeyQueryGateway = access_key_queries

    async def __call__(self, request: LogoutAllUserRequest):
        try:
            found_key: AccessKey = await self._access_key_queries.by_id(
                request.access_key_id
            )
        except AccessKeyNotFound:
            return
        
        await self._access_key_commands.delete_keys_by_user_id(found_key.user_id)
        