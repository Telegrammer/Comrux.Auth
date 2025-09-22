from contextlib import asynccontextmanager
from dishka import make_async_container, AsyncContainer

import uvicorn
import dishka.integrations.fastapi as fastapi_integration
from dishka.integrations.fastapi import FromDishka, inject
import dishka.integrations.faststream as faststream_integration
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from faststream import FastStream
from faststream.redis import RedisBroker

from setup import (
    Settings,
    settings,
    DatabaseHelper,
    DatabaseProvider,
    ApplicationProvider,
    DomainProvider,
    PresentationProvider,
)
from domain import UserService

from presentation.http.controllers.user import user_router
from presentation.http.middleware import InjectCurrentUserIdMiddleware

from infrastructure.subscribers import user_sub_router

origins = ["http://localhost:8000", "http://127.0.0.1:3000", "http://localhost:3000"]

broker = RedisBroker(str(settings.cache.url))

container: AsyncContainer = make_async_container(
    DatabaseProvider(),
    DomainProvider(),
    ApplicationProvider(),
    PresentationProvider(),
    context={Settings: settings, RedisBroker: broker},
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with container() as app_state:
        app.state.container = app_state
        await broker.start()
    yield

    db_helper = await container.get(DatabaseHelper)
    await db_helper.dispose()
    await broker.stop()


broker.include_router(user_sub_router)
faststream_integration.setup_dishka(container, FastStream(broker))


auth_app = FastAPI(lifespan=lifespan)
auth_app.include_router(user_router)
auth_app.add_middleware(InjectCurrentUserIdMiddleware)
auth_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi_integration.setup_dishka(container=container, app=auth_app)


@auth_app.get("/")
@inject
async def root(service: FromDishka[UserService]):
    return {"service": service.__repr__()}


if __name__ == "__main__":
    uvicorn.run(
        "main:auth_app", host=settings.run.host, port=settings.run.port, reload=True
    )
