__all__ = ["InjectCurrentUserIdMiddleware"]


from faststream import BaseMiddleware
from faststream.types import DecodedMessage
from domain import UserId
from .update_context import update_context
class InjectCurrentUserIdMiddleware(BaseMiddleware):

    def __init__(self, msg = None):
        super().__init__(msg)

    async def on_consume(self, msg: DecodedMessage) -> DecodedMessage:
        user_id: UserId = UserId(msg.__dict__.get("_decoded_body").get("user_id"))
        await update_context({UserId: user_id})
        return msg