from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.jwt import decode_access_token
from app.core.db import get_session
from app.models.sadaqa import CompanyAuth, Company

security = HTTPBearer(auto_error=False)

async def get_current_sadaqa_company(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_session)
):

    if not credentials:
        raise HTTPException(status_code=401, detail="Authorization required")

    token = credentials.credentials


    payload = decode_access_token(token)

    role = payload.get("role")
    if role != "company":
        raise HTTPException(status_code=403, detail="Company access required")

    auth_id = payload.get("company_auth_id")
    if not auth_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    result = await db.execute(
        select(CompanyAuth).where(CompanyAuth.id == auth_id)
    )
    auth = result.scalar_one_or_none()

    if not auth:
        raise HTTPException(status_code=401, detail="Auth not found")

    if not auth.is_active:
        raise HTTPException(status_code=403, detail="Company is inactive")


    result = await db.execute(
        select(Company).where(Company.id == auth.company_id)
    )
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(status_code=401, detail="Company not found")

    return company