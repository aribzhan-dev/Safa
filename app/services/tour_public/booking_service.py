from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.tours import Tours, BookingTour
from app.schemas.tour_schemas import BookingCreate
import random, string


def generate_secret_code() -> str:
    return "".join(random.choices(string.digits, k=6))


async def create_public_booking(
    db: AsyncSession,
    data: BookingCreate
):
    result = await db.execute(
        select(Tours).where(Tours.id == data.tour_id)
    )
    tour = result.scalar_one_or_none()

    if not tour:
        raise HTTPException(404, "Tour not found")

    secret_code = generate_secret_code()
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
        secret_code=secret_code,
    )

    db.add(booking)
    await db.commit()
    await db.refresh(booking)

    return booking