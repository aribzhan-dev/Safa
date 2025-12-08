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



    if not Authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid Authorization header")

    token = Authorization.split(" ")[1]


    payload = decode_access_token(token)

    auth_id = payload.get("company_auth_id")
    if not auth_id:
        raise HTTPException(401, "Invalid sadaqa token, missing company_auth_id")


    result = await db.execute(
        select(CompanyAuth).where(CompanyAuth.id == auth_id)
    )
    auth: CompanyAuth = result.scalar_one_or_none()

    if not auth:
        raise HTTPException(401, "Auth record not found")

    if not auth.is_active:
        raise HTTPException(403, "Company is inactive")


    result = await db.execute(
        select(Company).where(Company.id == auth.company_id)
    )
    company: Company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(401, "Company not found")

    return company