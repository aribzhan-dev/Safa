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



async def create_category(db: AsyncSession, data: TourCategoryCreate):
    category = TourCategories(**data.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def get_category(db: AsyncSession, category_id: int):
    result = await db.execute(
        select(TourCategories).where(TourCategories.id == category_id)
    )
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category



async def get_categories(db: AsyncSession):
    result = await db.execute(select(TourCategories))
    return result.scalars().all()



async def update_category(db: AsyncSession, category_id: int, data: TourCategoryUpdate):
    category = await get_category(db, category_id)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(category, key, value)

    await db.commit()
    await db.refresh(category)
    return category



async def create_guide(db: AsyncSession, data: TourGuideCreate):
    guide = TourGuides(**data.model_dump())
    db.add(guide)
    await db.commit()
    await db.refresh(guide)
    return guide


async def get_guide(db: AsyncSession, guide_id: int):
    result = await db.execute(
        select(TourGuides).where(TourGuides.id == guide_id)
    )
    guide = result.scalar_one_or_none()

    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")

    return guide


async def get_guides(db: AsyncSession):
    result = await db.execute(select(TourGuides))
    return result.scalars().all()


async def update_guide(db: AsyncSession, guide_id: int, data: TourGuideUpdate):
    guide = await get_guide(db, guide_id)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(guide, key, value)

    await db.commit()
    await db.refresh(guide)
    return guide



async def create_tour(db: AsyncSession, data: TourCreate):
    await get_company(db, data.tour_company_id)
    await get_category(db, data.tour_category_id)
    await get_guide(db, data.tour_guid_id)

    tour = Tours(**data.model_dump())
    db.add(tour)
    await db.commit()
    await db.refresh(tour)
    return tour



async def get_tour(db: AsyncSession, tour_id: int):
    result = await db.execute(
        select(Tours).where(Tours.id == tour_id)
    )
    tour = result.scalar_one_or_none()

    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")

    return tour



async def get_tours(db: AsyncSession, company_id: int | None = None):
    query = select(Tours)

    if company_id is not None:
        query = query.where(Tours.tour_company_id == company_id)

    result = await db.execute(query)
    return result.scalars().all()



async def update_tour(db: AsyncSession, tour_id: int, data: TourUpdate):
    tour = await get_tour(db, tour_id)
    payload = data.model_dump(exclude_unset=True)

    if "tour_company_id" in payload:
        await get_company(db, payload["tour_company_id"])

    if "tour_category_id" in payload:
        await get_category(db, payload["tour_category_id"])

    if "tour_guid_id" in payload:
        await get_guide(db, payload["tour_guid_id"])

    for key, value in payload.items():
        setattr(tour, key, value)

    await db.commit()
    await db.refresh(tour)
    return tour