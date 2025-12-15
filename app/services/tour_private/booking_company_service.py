from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tours import BookingTour, Tours
from app.models.tours import TourCompanies


async def get_company_bookings(
    db: AsyncSession,
    company: TourCompanies
):
    result = await db.execute(
        select(BookingTour)
        .join(Tours)
        .where(Tours.tour_company_id == company.id)
    )
    return result.scalars().all()