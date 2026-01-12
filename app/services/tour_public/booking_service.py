from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
import random, string

from app.models.tours import Tours, BookingTour
from app.schemas.tour_schemas import BookingCreate
# from app.services.notification_service import notify_tour_company


def generate_secret_code() -> str:
    return "".join(random.choices(string.digits, k=6))


async def create_public_booking(
    db: AsyncSession,
    data: BookingCreate
):
    tour = await db.scalar(
        select(Tours).where(Tours.id == data.tour_id)
    )
    if not tour:
        raise HTTPException(404, "Tour not found")

    booking = BookingTour(
        tour_id=data.tour_id,
        person_number=data.person_number,
        name=data.name,
        surname=data.surname,
        patronymic=data.patronymic,
        phone=data.phone,
        email=data.email,
        passport_number=data.passport_number,
        date_of_birth=data.date_of_birth,
        secret_code=generate_secret_code(),
    )

    db.add(booking)
    await db.commit()
    await db.refresh(booking)

    # await notify_tour_company(
    #     db=db,
    #     tour_company_id=tour.tour_company_id,
    #     title="New booking request",
    #     body=f"{data.name} {data.surname} booked for tour",
    #     type_="booking",
    # )

    return booking