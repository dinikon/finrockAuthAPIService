import hashlib
import hmac


def validate_telegram_auth(data: dict, bot_token: str) -> bool:
    check_string = "\n".join(
        [f"{key}={data[key]}" for key in sorted(data) if key != "hash"]
    )
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(
        secret_key, check_string.encode(), hashlib.sha256
    ).hexdigest()
    is_valid = calculated_hash == data["hash"]

    # if is_valid:
    #     print("Данные прошли валидацию и подлинны:", data)
    # else:
    #     print("Ошибка валидации данных! Полученные данные:", data)
    #     print("Calculated Hash:", calculated_hash)
    #     print("Received Hash:", data['hash'])

    return is_valid
