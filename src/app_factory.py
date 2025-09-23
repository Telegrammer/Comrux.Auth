from contextlib import asynccontextmanager
from dishka import make_async_container, AsyncContainer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from faststream import FastStream
from faststream.redis import RedisBroker
import dishka.integrations.fastapi as fastapi_integration
import dishka.integrations.faststream as faststream_integration
import logging, os

from setup import (
    Settings,
    settings,
    DatabaseHelper,
    DatabaseProvider,
    ApplicationProvider,
    DomainProvider,
    PresentationProvider,
)
from presentation.http.controllers.user import user_router
from presentation.http.middleware import InjectCurrentUserIdMiddleware as InjectRequestCurrentUserId
from infrastructure.subscribers.user import sub_router
from infrastructure.subscribers.middleware import InjectCurrentUserIdMiddleware as InjectMessageCurrentUserId


logger = logging.getLogger("app_factory")
logger.setLevel(logging.INFO)

def create_app() -> FastAPI:
    print("created")
    broker = RedisBroker(str(settings.cache.url))
    container: AsyncContainer = make_async_container(
        DatabaseProvider(),
        DomainProvider(),
        ApplicationProvider(),
        PresentationProvider(),
        context={Settings: settings, RedisBroker: broker},
    )

    broker.include_router(sub_router)
    faststream_integration.setup_dishka(container, FastStream(broker))
    broker.add_middleware(InjectMessageCurrentUserId)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        async with container() as app_state:
            app.state.container = app_state
            await broker.start()
        yield
        db_helper = await container.get(DatabaseHelper)
        await db_helper.dispose()
        await broker.stop()

    app = FastAPI(lifespan=lifespan)

    app.include_router(user_router)
    app.add_middleware(InjectRequestCurrentUserId)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8000", "http://127.0.0.1:3000", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    fastapi_integration.setup_dishka(container=container, app=app)
    return app
