from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.sadaqa import Company, CompanyAuth
from app.schemas.sadaqa_schemas import CompanyCreate, CompanyUpdate
from app.core.security import verify_password, hash_password
from app.core.jwt import create_tokens, decode_access_token, decode_refresh_token





async def create_company(
        db: AsyncSession,
        data: CompanyCreate
):
    company = Company(
        title=data.title,
        why_collecting=data.why_collecting,
        image=data.image,
        payment=data.payment,
    )
    db.add(company)
    await db.flush()

    auth = CompanyAuth(
        company_id=company.id,
        login=data.login,
        password_hash=hash_password(data.password)
    )
    db.add(auth)
    await db.commit()
    await db.refresh(company)

    access, refresh = create_tokens({
        "company_auth_id": auth.id,
        "role": "company"
    })

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "Bearer"
    }

async def login_company(
        db: AsyncSession,
        login: str,
        password: str
):
    result = await db.execute(
        select(CompanyAuth).where(CompanyAuth.login == login)
    )
    auth = result.scalar_one_or_none()

    if not auth or not verify_password(password, auth.password_hash):
        raise HTTPException(401, "Invalid login or password")

    access, refresh = create_tokens({
        "company_auth_id": auth.id,
        "role": "company"
    })

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "Bearer"
    }



async def refresh_tokens(refresh_token: str):
    payload = decode_refresh_token(refresh_token)

    if not payload:
        raise HTTPException(401, "Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(401, "Not a refresh token")

    new_payload = {
        "company_auth_id": payload["company_auth_id"],
        "role": payload["role"],
    }

    access, refresh = create_tokens(new_payload)

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "Bearer"
    }


async def update_company(
    db: AsyncSession,
    company_id: int,
    data: CompanyUpdate
):
    company = await db.get(Company, company_id)
    if not company:
        raise HTTPException(404, "Company not found")

    payload = data.model_dump(exclude_unset=True)

    if "payment" in payload:
        exists = await db.execute(
            select(Company.id).where(
                Company.payment == payload["payment"],
                Company.id != company_id
            )
        )
        if exists.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="This payment link is already used by another company"
            )

    for k, v in payload.items():
        setattr(company, k, v)

    await db.commit()
    await db.refresh(company)
    return company