import logging

from fastapi import APIRouter, HTTPException

from auth.utils import validate_telegram_auth
from schemas.auth import TelegramAuthData


log = logging.getLogger(__name__)


router = APIRouter(
    tags=["auth"],
)


@router.post("/login")
async def auth(data: TelegramAuthData):
    data_dict = data.dict()

    log.info("Received data for authentication: %s", data_dict)

    if validate_telegram_auth(
        data_dict, "6743079497:AAE1ZY9QPKiDnZxufcoipXxVVWNQ-vTAPEQ"
    ):
        return {"status": "success", "message": "User authenticated successfully!"}
    else:
        raise HTTPException(status_code=403, detail="Invalid data!")
