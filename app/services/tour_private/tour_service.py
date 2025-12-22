from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.tours import Tours, TourCompanies
from app.schemas.tour_schemas import TourCreate, TourUpdate
from datetime import datetime


def normalize_dt(dt: datetime | None):
    if dt and dt.tzinfo:
        return dt.replace(tzinfo=None)
    return dt


async def create_tour(db: AsyncSession, company: TourCompanies, data: TourCreate):
    payload = data.model_dump()
    payload["departure_date"] = normalize_dt(payload.get("departure_date"))
    payload["return_date"] = normalize_dt(payload.get("return_date"))

    tour = Tours(
        tour_company_id=company.id,
        **payload
    )
    db.add(tour)
    await db.commit()
    await db.refresh(tour)
    return tour


async def get_tours(db: AsyncSession, company: TourCompanies):
    r = await db.execute(
        select(Tours).where(Tours.tour_company_id == company.id)
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

    payload = data.model_dump(exclude_unset=True)

    if "departure_date" in payload:
        payload["departure_date"] = normalize_dt(payload["departure_date"])

    if "return_date" in payload:
        payload["return_date"] = normalize_dt(payload["return_date"])

    for k, v in payload.items():
        setattr(tour, k, v)

    await db.commit()
    await db.refresh(tour)
    return tour