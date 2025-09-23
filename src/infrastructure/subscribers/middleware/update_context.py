from faststream import context
from dishka import AsyncContainer
from typing import Type

from utils.merge_context import merge_context


async def update_context(new_context: dict[Type, object]) -> None:
    old_container: AsyncContainer = context.get_local("dishka")
    app_container: AsyncContainer = old_container.parent_container
    async with app_container(context=merge_context(old_container, new_context)) as new_container:
        context.set_local("dishka", new_container)
