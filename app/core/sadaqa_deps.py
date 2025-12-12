from fastapi import Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.jwt import decode_access_token
from app.core.db import get_session
from app.models.sadaqa import CompanyAuth, Company


async def get_current_sadaqa_company(
    authorization: str | None = Header(default=None),
    db: AsyncSession = Depends(get_session)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Access token required")

    token = authorization.strip()

    payload = decode_access_token(token)

    auth_id = payload.get("company_auth_id")
    if not auth_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(
        select(CompanyAuth).where(CompanyAuth.id == auth_id)
    )
    auth = result.scalar_one_or_none()

    if not auth:
        raise HTTPException(status_code=401, detail="Auth record not found")

    if not auth.is_active:
        raise HTTPException(status_code=403, detail="Company is inactive")


    result = await db.execute(
        select(Company).where(Company.id == auth.company_id)
    )
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(status_code=401, detail="Company not found")

    return company