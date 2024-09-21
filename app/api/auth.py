import logging

from fastapi import APIRouter, HTTPException

from auth.utils import validate_telegram_auth
from schemas.auth import TelegramAuthData

logger = logging.getLogger("auth_logger")

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def auth(data: TelegramAuthData):
    data_dict = data.dict()

    # Логирование входных данных
    logger.info("Received auth request with data: %s", data_dict)

    try:
        # Валидация данных
        if validate_telegram_auth(data_dict, "YOUR_BOT_TOKEN"):
            logger.info("Authentication successful for user: %s", data.first_name)
            return {"status": "success", "message": "User authenticated successfully!"}
        else:
            logger.warning("Authentication failed for user: %s", data.first_name)
            raise HTTPException(status_code=403, detail="Invalid data!")
    except Exception as e:
        logger.error("Error during authentication: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")
