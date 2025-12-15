from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.tours import TourCategories, TourCompanies
from app.schemas.tour_schemas import TourCategoryCreate, TourCategoryUpdate


async def create_category(
    db: AsyncSession,
    company: TourCompanies,
    data: TourCategoryCreate
):
    category = TourCategories(
        tour_company_id=company.id,
        title=data.title
    )
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def get_categories(db: AsyncSession, company: TourCompanies):
    r = await db.execute(
        select(TourCategories).where(
            TourCategories.tour_company_id == company.id
        )
    )
    return r.scalars().all()


async def update_category(
    db: AsyncSession,
    category_id: int,
    data: TourCategoryUpdate,
    company: TourCompanies
):
    r = await db.execute(
        select(TourCategories).where(
            TourCategories.id == category_id,
            TourCategories.tour_company_id == company.id
        )
    )
    category = r.scalar_one_or_none()

    if not category:
        raise HTTPException(404, "Category not found")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(category, k, v)

    await db.commit()
    await db.refresh(category)
    return category