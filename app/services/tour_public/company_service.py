from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tours import TourCompanies


async def get_public_companies(db: AsyncSession):
    result = await db.execute(
        select(
            TourCompanies.id,
            TourCompanies.comp_name,
            TourCompanies.logo,
            TourCompanies.rating
        )
    )
    return result.all()