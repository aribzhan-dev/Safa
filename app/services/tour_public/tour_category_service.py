from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tours import TourCategories


async def get_public_categories(db: AsyncSession):
    result = await db.execute(
        select(
            TourCategories.id,
            TourCategories.title
        )
    )
    return result.mappings().all()