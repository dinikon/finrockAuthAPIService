import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import settings

from api import auth

app = FastAPI()
app.include_router(auth.router, prefix=settings.api.prefix)

origins = [
    "http://localhost:5173",
]

methods = [
    "DELETE",
    "GET",
    "POST",
    "PUT",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=["*"],
)


# @app.on_event("startup")
# async def startup():
#     await database.connect()
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     if database.is_connected:
#         await database.disconnect()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
