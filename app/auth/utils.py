import hashlib
import hmac
from datetime import datetime, timedelta
from jose import jwt
from core.config import settings


def validate_telegram_auth(data: dict, bot_token: str) -> bool:
    check_string = "\n".join(
        [f"{key}={data[key]}" for key in sorted(data) if key != "hash"]
    )
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(
        secret_key, check_string.encode(), hashlib.sha256
    ).hexdigest()
    is_valid = calculated_hash == data["hash"]

    return is_valid


async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.jwt.access_token_expire_minutes
    )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt.access_token_secret,
        algorithm="HS256",
    )
    return encoded_jwt


async def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.jwt.refresh_token_expire_minutes
    )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt.refresh_token_secret,
        algorithm="HS256",
    )
    return encoded_jwt
