from fastapi import Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.jwt import decode_access_token
from app.core.db import get_session
from app.models.tours import TourCompanies
from sqlalchemy import select


async def get_current_company(
    Authorization: str = Header(...),
    db: AsyncSession = Depends(get_session)
):

    if not Authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid Authorization header")

    token = Authorization.split(" ")[1]
    payload = decode_access_token(token)

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