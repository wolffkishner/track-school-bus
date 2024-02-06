from fastapi import Header, HTTPException
from jwt import decode_jwt, SECRET_KEY


# RBAC Functions
async def verify(role, token: str = Header(alias="Bearer")):
    if token is None:
        raise HTTPException(status_code=401, detail="Token not found")
    try:
        decoded = decode_jwt(token, SECRET_KEY)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid token")
    if decoded["role"] != role:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return decoded["id"]


verify_admin = verify("admin")
verify_driver = verify("driver")
verify_student = verify("student")
