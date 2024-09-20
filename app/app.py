
import os

import uvicorn
from fastapi import FastAPI, HTTPException
import hashlib
import hmac

from schemas.auth import TelegramAuthData

app = FastAPI()
app.include_router(auth.router, prefix="/api")

BOT_TOKEN = os.getenv("BOT_TOKEN", "6743079497:AAE1ZY9QPKiDnZxufcoipXxVVWNQ-vTAPEQ")


@app.post("/auth/login")
async def auth(data: TelegramAuthData):
    data_dict = data.dict()
    if validate_telegram_auth(data_dict, BOT_TOKEN):
        return {"status": "success", "message": "User authenticated successfully!"}
    else:
        raise HTTPException(status_code=403, detail="Invalid data!")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug", reload=True)