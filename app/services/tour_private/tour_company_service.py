from app.schemas.tour_schemas import TourCompanyCreate, TourCompanyUpdate
from app.core.jwt import create_tokens, decode_refresh_token
from app.core.security import hash_password, verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tours import TourCompanies
from fastapi import HTTPException
from sqlalchemy import select


async def create_company(db: AsyncSession, data: TourCompanyCreate):
    exists = await db.execute(
        select(TourCompanies).where(TourCompanies.username == data.username)
    )
    if exists.scalar_one_or_none():
        raise HTTPException(400, "Username already exists")

    company = TourCompanies(
        username=data.username,
        password_hash=hash_password(data.password),
        logo=data.logo,
        comp_name=data.comp_name,
        rating=data.rating,
    )

    db.add(company)
    await db.flush()

    access, refresh = create_tokens({
        "company_id": company.id,
        "role": "tour_company"
    })
    await db.commit()
    await db.refresh(company)
    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "Bearer"
    }



async def login_company(db: AsyncSession, username: str, password: str):
    result = await db.execute(
        select(TourCompanies).where(TourCompanies.username == username)
    )
    company = result.scalar_one_or_none()

    if not company or not verify_password(password, company.password_hash):
        raise HTTPException(401, "Invalid username or password")

    access, refresh = create_tokens({
        "company_id": company.id,
        "role": "tour_company"
    })

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "Bearer"
    }


async def refresh_tokens(db: AsyncSession, refresh_token: str):
    payload = decode_refresh_token(refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(401, "Not a refresh token")

    company_id = payload.get("company_id")

    result = await db.execute(
        select(TourCompanies).where(TourCompanies.id == company_id)
    )
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(401, "Company not found")

    access, refresh = create_tokens({
        "company_id": company.id,
        "role": "tour_company"
    })

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "Bearer"
    }



async def update_company(db: AsyncSession, company: TourCompanies, data: TourCompanyUpdate):
    payload = data.model_dump(exclude_unset=True)

    if "password" in payload:
        payload["password_hash"] = hash_password(payload.pop("password"))

    for k, v in payload.items():
        setattr(company, k, v)

    await db.commit()
    await db.refresh(company)
    return company