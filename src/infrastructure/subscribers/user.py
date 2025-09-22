__all__ = ["sub_router"]


from pydantic import BaseModel
from datetime import datetime
from dishka import AsyncContainer
from dishka.integrations.faststream import FromDishka, inject

from faststream.redis import RedisRouter
from faststream import BaseMiddleware


from domain import UserId
from application import UnitOfWork, LogoutAllUsecase

sub_router = RedisRouter()

class UserSensetiveDataChange(BaseModel):
    user_id: str
    changed_fields: str
    occured: datetime


@sub_router.subscriber(stream="user:sensetive_data_changed")
@inject
async def logout_all(container: FromDishka[AsyncContainer], message: UserSensetiveDataChange):
    async with container.parent_container(context={UserId: UserId(message.user_id)}) as request_container:
        uow: UnitOfWork = await request_container.get(UnitOfWork)
        usecase: LogoutAllUsecase = await request_container.get(LogoutAllUsecase)
        async with uow:
            await usecase()
