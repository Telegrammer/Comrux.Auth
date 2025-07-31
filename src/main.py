from contextlib import asynccontextmanager


import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.models import Base
from setup import settings, db_helper

from automapper import mapper

from presentation.http.controllers.user import router as user_router

origins = ["http://localhost:8000", "http://127.0.0.1:3000", "http://localhost:3000"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield

    await db_helper.dispose()


auth_app = FastAPI(lifespan=lifespan)

auth_app.include_router(user_router)
auth_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@auth_app.get("/")
async def root():
    return {"opa": "Amerika evropa"}


if __name__ == "__main__":
    uvicorn.run(
        "main:auth_app", host=settings.run.host, port=settings.run.port, reload=True
    )
