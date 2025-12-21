import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

SECRET_KEY = "super_secret_key_change_this_to_random_32_char"
REFRESH_SECRET_KEY = "super_refresh_secret_key_change_this_to_random_32_char"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 120
REFRESH_TOKEN_EXPIRE_DAYS = 30


def create_access_token(data: dict):
    payload = data.copy()
    payload.update({
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "type": "access"
    })
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    payload = data.copy()
    payload.update({
        "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "type": "refresh"
    })
    return jwt.encode(payload, REFRESH_SECRET_KEY, algorithm=ALGORITHM)


def create_tokens(data: dict):
    return (
        create_access_token(data),
        create_refresh_token(data)
    )


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"require": ["exp", "type"]}
        )

        if payload["type"] != "access":
            raise HTTPException(401, "Not an access token")

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Access token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid access token")


def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(
            token,
            REFRESH_SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"require": ["exp", "type"]}
        )

        if payload["type"] != "refresh":
            raise HTTPException(401, "Not a refresh token")

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Refresh token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid refresh token")
