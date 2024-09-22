from pydantic import BaseModel


class TelegramAuthData(BaseModel):
    id: int
    first_name: str
    username: str
    photo_url: str
    auth_date: int
    hash: str


class Token(BaseModel):
    access_token: str
    token_type: str
