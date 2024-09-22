import logging
from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, HTTPException, Response, Request
from jose import jwt

from auth.utils import validate_telegram_auth, create_access_token, create_refresh_token
from core.config import settings
from schemas.auth import TelegramAuthData, Token

log = logging.getLogger(__name__)


router = APIRouter(
    tags=["auth"],
)


@router.post("/login")
async def auth(
        response: Response,
        data: TelegramAuthData):
    data_dict = data.dict()

    log.info("Start authentication process for username: %s", data_dict.get("username"))

    # Логируем полученные данные
    log.debug("Received data for authentication: %s", data_dict)

    # Логируем процесс валидации
    if validate_telegram_auth(
            data_dict, "6743079497:AAE1ZY9QPKiDnZxufcoipXxVVWNQ-vTAPEQ"
    ):
        log.info("Validation successful for username: %s", data_dict.get("username"))

        try:
            # Логируем процесс создания access token
            access_token = await create_access_token(data={"username": data_dict["username"]})
            log.debug("Access token generated for username: %s", data_dict.get("username"))

            # Логируем процесс создания refresh token
            refresh_token = await create_refresh_token(data={"username": data_dict["username"]})
            log.debug("Refresh token generated for username: %s", data_dict.get("username"))

            # Установка времени истечения cookie
            expire_time = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt.refresh_token_expire_minutes)

            # Логируем процесс установки cookies
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                samesite="strict",
                secure=False,
                expires=expire_time,
            )
            log.info("Refresh token cookie set for username: %s with expiration time: %s",
                     data_dict.get("username"), expire_time)

            # Возвращаем access токен
            return Token(
                access_token=access_token,
                token_type="Bearer",
            )

        except Exception as e:
            log.error("Error occurred during token generation or cookie setting: %s", str(e))
            raise HTTPException(status_code=500, detail="Internal server error during authentication")

    else:
        log.warning("Validation failed for username: %s", data_dict.get("username"))
        raise HTTPException(status_code=403, detail="Invalid data!")


@router.post("/refresh", response_model=Token)
async def refresh(
    request: Request,
    response: Response,
):
    log.info("Received token refresh request")

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Логируем получение refresh token из cookies
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            log.warning("No refresh token found in cookies")
            raise credentials_exception
        log.debug("Refresh token received from cookies: %s", refresh_token)

        # Логируем процесс декодирования refresh token
        payload = jwt.decode(
            refresh_token,
            settings.jwt.refresh_token_secret,
            algorithms=["HS256"],
        )
        log.debug("Decoded refresh token payload: %s", payload)

        username: str = payload.get("username")
        if username is None:
            log.warning("Username not found in token payload")
            raise credentials_exception
        log.info("Successfully validated token for username: %s", username)

    except Exception as e:
        log.error("Error during token validation: %s", str(e))
        credentials_exception.detail = str(e)
        raise credentials_exception

    try:
        # Логируем процесс создания нового access token
        access_token = await create_access_token(data={"username": username})
        log.debug("New access token generated for username: %s", username)

        # Логируем процесс создания нового refresh token
        refresh_token = await create_refresh_token(data={"username": username})
        log.debug("New refresh token generated for username: %s", username)

        # Устанавливаем время истечения cookies
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt.refresh_token_expire_minutes)
        log.info("Setting new refresh token cookie with expiration: %s", expire_time)

        # Логируем процесс установки cookies
        response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=True,
            samesite="strict",
            secure=False,
            expires=expire_time,
        )
        log.info("Refresh token cookie set successfully for username: %s", username)

        return Token(
            access_token=access_token,
            token_type="Bearer",
        )

    except Exception as e:
        log.error("Error occurred during token generation or cookie setting: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal server error during token refresh")


@router.post("/logout")
async def logout(response: Response):
    log.info("Received logout request")

    try:
        # Логируем удаление refresh token из cookies
        response.delete_cookie("refresh_token")
        log.info("Refresh token cookie deleted successfully")

        return {"message": "Logout successfully"}

    except Exception as e:
        log.error("Error during logout: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal server error during logout")
