from fastapi import HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError

import os
print(os.listdir())

with open("public_key.pem", "r") as f:
    PUBLIC_KEY_AUTH = f.read()

auth = HTTPBearer()


def verify_token(token: str):
    """
    Verify JWT token and return decoded token. Raise HTTPException if token is invalid
    :param token:
    :return: decoded token
    :raise HTTPException: if token is invalid
    """
    try:
        decoded = jwt.decode(token, PUBLIC_KEY_AUTH, algorithms=["RS256"])
        return decoded
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
