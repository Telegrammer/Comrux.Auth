__all__ = ["sub_router"]


from dishka.integrations.faststream import FromDishka, inject
from faststream.redis import RedisRouter, StreamSub

from application import UnitOfWork, LogoutAllUsecase
from utils import generate_consumer_id

from .models.user import UserSensetiveDataChange

sub_router = RedisRouter()


@sub_router.subscriber(
    stream=StreamSub(
        "user:sensetive_data_changed",
        group="user-group",
        consumer=generate_consumer_id(),
        last_id=">",
    )
)
@inject
async def logout_all(
    uow: FromDishka[UnitOfWork],
    usecase: FromDishka[LogoutAllUsecase], 
    message: UserSensetiveDataChange
):
    async with uow:
        await usecase()
    return True