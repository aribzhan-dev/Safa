from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.tours import (
    TourCompanies, TourCategories, TourGuides, Tours
)
from app.schemas.tour_schemas import (
    TourCompanyCreate, TourCompanyUpdate,
    TourCategoryCreate, TourCategoryUpdate,
    TourGuideCreate, TourGuideUpdate,
    TourCreate, TourUpdate
)


async def create_company(db: AsyncSession, data: TourCompanyCreate):
    company = TourCompanies(**data.model_dump())
    db.add(company)
    await db.commit()
    await db.refresh(company)
    return company


async def get_company(db: AsyncSession, company_id: int):
    result = await db.execute(
        select(TourCompanies).where(TourCompanies.id == company_id)
    )
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return company


async def get_companies(db: AsyncSession):
    result = await db.execute(select(TourCompanies))
    return result.scalars().all()


async def update_company(db: AsyncSession, company_id: int, data: TourCompanyUpdate):
    company = await get_company(db, company_id)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(company, key, value)

    await db.commit()
    await db.refresh(company)
    return company