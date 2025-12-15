from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.tours import TourGuides, TourCompanies
from app.schemas.tour_schemas import TourGuideCreate, TourGuideUpdate


async def create_guide(db: AsyncSession, company: TourCompanies, data: TourGuideCreate):
    guide = TourGuides(
        tour_company_id=company.id,
        **data.model_dump()
    )
    db.add(guide)
    await db.commit()
    await db.refresh(guide)
    return guide


async def get_guides(db: AsyncSession, company: TourCompanies):
    r = await db.execute(
        select(TourGuides).where(
            TourGuides.tour_company_id == company.id
        )
    )
    return r.scalars().all()


async def update_guide(
    db: AsyncSession,
    guide_id: int,
    data: TourGuideUpdate,
    company: TourCompanies
):
    r = await db.execute(
        select(TourGuides).where(
            TourGuides.id == guide_id,
            TourGuides.tour_company_id == company.id
        )
    )
    guide = r.scalar_one_or_none()

    if not guide:
        raise HTTPException(404, "Guide not found")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(guide, k, v)

    await db.commit()
    await db.refresh(guide)
    return guide