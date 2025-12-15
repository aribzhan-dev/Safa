from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tours import Tours


async def get_public_tours(db: AsyncSession):
    result = await db.execute(
        select(
            Tours.id,
            Tours.tour_company_id,
            Tours.tour_category_id,
            Tours.tour_guid_id,
            Tours.image,
            Tours.price,
            Tours.departure_date,
            Tours.return_date,
            Tours.duration,
            Tours.is_new,
            Tours.max_people,
            Tours.location
        )
    )
    return result.mappings().all()