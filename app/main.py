import logging
from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from core.config import settings

from api import router as api_router
from core.models.db_helper import db_helper
from core.models import TelegramClient


logging.basicConfig(
    # level=logging.INFO,
    format=settings.logging.log_format,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(TelegramClient.metadata.create_all)
    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()


main_app = FastAPI(
    default_response_class=ORJSONResponse,
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


main_app.include_router(
    api_router,
)


if __name__ == "__main__":
    uvicorn.run("main:main_app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True)
