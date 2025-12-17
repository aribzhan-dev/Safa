from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.jwt import decode_access_token
from app.core.db import get_session
from app.models.tours import TourCompanies

security = HTTPBearer(auto_error=False)

async def get_current_tour_company(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_session)
):
    if not credentials:
        raise HTTPException(401, "Authorization required")

    payload = decode_access_token(credentials.credentials)

    if payload.get("role") != "tour_company":
        raise HTTPException(403, "Invalid role")

    company_id = payload.get("company_id")
    if not company_id:
        raise HTTPException(401, "Invalid token")

    result = await db.execute(
        select(TourCompanies).where(TourCompanies.id == company_id)
    )
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(401, "Company not found")

    return company