import logging

import uvicorn

from starlette.middleware.cors import CORSMiddleware

from core.config import settings

from api import router as api_router
from create_fastapi_app import create_app


logging.basicConfig(
    level=settings.logging.log_level,
    format=settings.logging.log_format,
)

main_app = create_app()


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
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )

