from jose import jwt
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("DRIVER_TRACKER_SECRET_KEY") or "secret"


def create_jwt(payload, secret_key=SECRET_KEY):
    try:
        payload["exp"] = datetime.utcnow() + timedelta(days=15)
        token = jwt.encode(payload, secret_key, algorithm="HS256")
    except Exception as e:
        raise e
    return token


def decode_jwt(token, secret_key=SECRET_KEY):
    try:
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
    except Exception as e:
        raise e
    return decoded
