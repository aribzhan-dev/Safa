from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.tours import Tours, TourCompanies
from app.schemas.tour_schemas import TourCreate, TourUpdate


async def create_tour(db: AsyncSession, company: TourCompanies, data: TourCreate):
    tour = Tours(
        tour_company_id=company.id,
        **data.model_dump()
    )
    db.add(tour)
    await db.commit()
    await db.refresh(tour)
    return tour


async def get_tours(db: AsyncSession, company: TourCompanies):
    r = await db.execute(
        select(Tours).where(
            Tours.tour_company_id == company.id
        )
    )
    return r.scalars().all()


async def update_tour(
    db: AsyncSession,
    tour_id: int,
    data: TourUpdate,
    company: TourCompanies
):
    r = await db.execute(
        select(Tours).where(
            Tours.id == tour_id,
            Tours.tour_company_id == company.id
        )
    )
    tour = r.scalar_one_or_none()

    if not tour:
        raise HTTPException(404, "Tour not found")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(tour, k, v)

    await db.commit()
    await db.refresh(tour)
    return tour