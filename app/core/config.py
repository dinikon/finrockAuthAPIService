from pydantic import BaseModel
from pydantic.v1 import BaseSettings


class RunConfig(BaseModel):
    host: str = "127.0.0.0"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()


settings = Settings()
