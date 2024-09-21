import logging

from fastapi import APIRouter, HTTPException
from auth.utils import validate_telegram_auth
from schemas.auth import TelegramAuthData

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def auth(data: TelegramAuthData):
    data_dict = data.dict()

    logger.info("Received data for authentication: %s", data_dict)

    if validate_telegram_auth(data_dict, "1231"):
        return {"status": "success", "message": "User authenticated successfully!"}
    else:
        raise HTTPException(status_code=403, detail="Invalid data!")
