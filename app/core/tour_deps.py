from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_session
from app.core.jwt import decode_access_token
from app.models.tours import TourCompanies

security = HTTPBearer()


async def get_current_tour_company(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_session),
):
    payload = decode_access_token(credentials.credentials)

    if payload.get("role") != "tour_company":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a tour company token",
        )

    company_id = payload.get("company_id")
    if not company_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    result = await db.execute(
        select(TourCompanies).where(TourCompanies.id == company_id)
    )
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Company not found",
        )

    return company