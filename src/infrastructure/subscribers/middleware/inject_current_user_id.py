__all__ = ["InjectCurrentUserIdMiddleware"]


from dishka import AsyncContainer
from faststream import BaseMiddleware, context
from faststream.types import DecodedMessage
from utils.merge_context import merge_context
from domain import UserId
from .update_context import update_context
class InjectCurrentUserIdMiddleware(BaseMiddleware):

    def __init__(self, msg = None):
        super().__init__(msg)

    async def on_consume(self, msg: DecodedMessage) -> DecodedMessage:
        user_id: UserId = UserId(msg.__dict__.get("_decoded_body").get("user_id"))

        old_container: AsyncContainer = context.get("dishka")
        app_conatiner: AsyncContainer = old_container.parent_container
        async with app_conatiner(context=merge_context(old_container, {UserId: user_id})) as new_container:
            context.set_local("dishka", new_container)
        return msg