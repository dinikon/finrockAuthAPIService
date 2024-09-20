import os

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import hashlib
import hmac

from schemas.auth import TelegramAuthData

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")


def validate_telegram_auth(data: dict, bot_token: str) -> bool:
    check_string = "\n".join([f"{key}={data[key]}" for key in sorted(data) if key != 'hash'])
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()
    is_valid = calculated_hash == data['hash']

    # Вывод данных в консоль
    if is_valid:
        print("Данные прошли валидацию и подлинны:", data)
    else:
        print("Ошибка валидации данных! Полученные данные:", data)
        print("Calculated Hash:", calculated_hash)
        print("Received Hash:", data['hash'])

    return is_valid


@app.post("/auth/login")
async def auth(data: TelegramAuthData):
    data_dict = data.dict()
    if validate_telegram_auth(data_dict, BOT_TOKEN):
        return {"status": "success", "message": "User authenticated successfully!"}
    else:
        raise HTTPException(status_code=403, detail="Invalid data!")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
