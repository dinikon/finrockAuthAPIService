from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import settings

from api import auth
from core.models.db_helper import db_helper
from core.models import TelegramClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(TelegramClient.metadata.create_all)
    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
)


origins = [
    "http://localhost:5173",
]


methods = [
    "DELETE",
    "GET",
    "POST",
    "PUT",
]


main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=["*"],
)


main_app.include_router(auth.router, prefix=settings.api.prefix)


if __name__ == "__main__":
    uvicorn.run("main:main_app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True)
