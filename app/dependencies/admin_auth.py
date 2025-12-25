from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.jwt import decode_access_token



security = HTTPBearer()

async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin only"
        )

    return payload