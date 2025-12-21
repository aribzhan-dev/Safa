from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.tour_deps import get_current_tour_company
from app.services.tour_private.booking_company_service import get_company_bookings

router = APIRouter(
    prefix="/bookings",
    tags=["Tour / Bookings (Private)"]
)
router.openapi_extra = {
    "security": [{"sadaqaAuth": []}]
}

@router.get("/")
async def my_bookings(
    db: AsyncSession = Depends(get_session),
    company = Depends(get_current_tour_company)
):
    return await get_company_bookings(db, company)