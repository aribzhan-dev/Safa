from app.core.security import verify_password, hash_password
from app.models.sadaqa import CompanyAuth, Company, Language
from app.schemas.tour_schemas import TourCompanyCreate
from app.schemas.sadaqa_schemas import LanguageCreate
from app.schemas.sadaqa_schemas import CompanyCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tours import TourCompanies
from app.core.jwt import create_tokens
from app.models.admin import Admin
from fastapi import HTTPException
from sqlalchemy import select

async def admin_login(
    db: AsyncSession,
    login: str,
    password: str
):
    admin = await db.scalar(
        select(Admin).where(Admin.login == login)
    )

    if not admin or not verify_password(password, admin.password_hash):
        raise HTTPException(401, "Invalid credentials")

    access, refresh = create_tokens({
        "admin_id": admin.id,
        "role": "admin"
    })

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "Bearer"
    }


async def create_tour_company(
    db: AsyncSession,
    data: TourCompanyCreate
):
    exists = await db.scalar(
        select(TourCompanies).where(TourCompanies.username == data.username)
    )
    if exists:
        raise HTTPException(400, "Username already exists")

    company = TourCompanies(
        username=data.username,
        password_hash=hash_password(data.password),
        logo=data.logo,
        comp_name=data.comp_name,
        rating=data.rating,
    )

    db.add(company)
    await db.commit()
    await db.refresh(company)

    return company



async def create_sadaqa_company(
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

    return company


async def create_language(db: AsyncSession, data: LanguageCreate):
    lang = Language(**data.model_dump())
    db.add(lang)
    await db.commit()
    await db.refresh(lang)
    return lang