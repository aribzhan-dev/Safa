from fastapi import Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.jwt import decode_access_token
from app.core.db import get_session
from app.models.sadaqa import CompanyAuth, Company


async def get_current_sadaqa_company(
        Authorization: str = Header(...),
        db: AsyncSession = Depends(get_session)
):
    token = Authorization

    if Authorization.startswith("Bearer "):
        token = Authorization.split(" ")[1]

    if not token:
        raise HTTPException(401, "Access token required")

    payload = decode_access_token(token)

    auth_id = payload.get("company_auth_id")
    if not auth_id:
        raise HTTPException(401, "Invalid sadaqa_routes token")

    result = await db.execute(
        select(CompanyAuth).where(CompanyAuth.id == auth_id)
    )
    auth = result.scalar_one_or_none()

    if not auth:
        raise HTTPException(401, "Auth record not found")

    if not auth.is_active:
        raise HTTPException(403, "Company is inactive")

    result = await db.execute(
        select(Company).where(Company.id == auth.company_id)
    )
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(401, "Company not found")

    return company
