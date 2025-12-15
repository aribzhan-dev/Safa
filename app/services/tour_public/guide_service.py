from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tours import TourGuides


async def get_public_guides(db: AsyncSession):
    result = await db.execute(
        select(
            TourGuides.id,
            TourGuides.name,
            TourGuides.surname,
            TourGuides.about_self,
            TourGuides.rating
        )
    )
    return result.mappings().all()