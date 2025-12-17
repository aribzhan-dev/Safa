from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas.tour_schemas import BookingCreate, BookingOut
from app.services.tour_public.booking_service import create_public_booking

router = APIRouter(
    prefix="/bookings",
    tags=["Tour / Booking (Public)"]
)

@router.post("/", response_model=BookingOut)
async def create_booking(
    data: BookingCreate,
    db: AsyncSession = Depends(get_session)
):
    return await create_public_booking(db, data)