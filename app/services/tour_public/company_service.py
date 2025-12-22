from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.models.tours import TourCompanies, Tours, StatusEnum


async def get_public_companies(db: AsyncSession):
    result = await db.execute(
        select(
            TourCompanies.id,
            TourCompanies.comp_name,
            TourCompanies.logo,
            TourCompanies.rating,
            func.count(Tours.id).label("active_tours_id")
        )
        .outerjoin(
            Tours,
            (Tours.tour_company_id == TourCompanies.id)
            & (Tours.status == StatusEnum.active)
        )
        .group_by(TourCompanies.id)
    )

    return [
        {
            "id": row.id,
            "comp_name": row.comp_name,
            "logo": row.logo,
            "rating": row.rating,
            "active_tours_id": row.active_tours_id or 0,
        }
        for row in result.all()
    ]



async def get_total_active_tours_count(db: AsyncSession) -> int:
    count = await db.scalar(
        select(func.count(Tours.id))
        .where(Tours.status == StatusEnum.active)
    )

    return int(count or 0)