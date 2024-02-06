from jose import jwt

SECRET_KEY = "secret"


def create_jwt(payload, secret_key=SECRET_KEY):
    try:
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
