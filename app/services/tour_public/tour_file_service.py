from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tours import TourFiles


async def get_public_tour_files(
    db: AsyncSession,
    tour_id: int
):
    result = await db.execute(
        select(
            TourFiles.id,
            TourFiles.file_name
        ).where(TourFiles.tour_id == tour_id)
    )
    return result.mappings().all()
