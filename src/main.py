from contextlib import asynccontextmanager
from dishka import make_async_container, AsyncContainer

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dishka.integrations.fastapi import setup_dishka, FromDishka, inject

from setup import Settings, DatabaseHelper, settings, DatabaseProvider, UsecaseProvider
from domain import UserService

from presentation.http.controllers.user import router as user_router

origins = ["http://localhost:8000", "http://127.0.0.1:3000", "http://localhost:3000"]


container: AsyncContainer = make_async_container(
    DatabaseProvider(), UsecaseProvider(), context={Settings: settings}
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with container() as app_state:
        app.state.container = app_state

    yield

    db_helper = await container.get(DatabaseHelper)
    await db_helper.dispose()


auth_app = FastAPI(lifespan=lifespan)
setup_dishka(container=container, app=auth_app)

auth_app.include_router(user_router)
auth_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@auth_app.get("/")
@inject
async def root(service: FromDishka[UserService]):
    return {"service": service.__repr__()}


if __name__ == "__main__":
    uvicorn.run(
        "main:auth_app", host=settings.run.host, port=settings.run.port, reload=True
    )
