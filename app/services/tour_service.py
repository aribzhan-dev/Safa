from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.tours import (
    TourCompanies, TourCategories,
    TourGuides, Tours, TourFiles,
    BookingTour
)
from app.schemas.tour_schemas import (
    TourCompanyCreate, TourCompanyUpdate,
    TourCategoryCreate, TourCategoryUpdate,
    TourGuideCreate, TourGuideUpdate,
    TourCreate, TourUpdate, TourFileCreate,
    BookingCreate,

)
from app.core.security import hash_password, verify_password
from app.core.jwt import create_tokens
import string, datetime,random


async def create_company(db: AsyncSession, data: TourCompanyCreate):
    exists = await db.execute(
        select(TourCompanies).where(TourCompanies.username == data.username)
    )
    if exists.scalar_one_or_none():
        raise HTTPException(400, "Username already exists")

    company = TourCompanies(
        username=data.username,
        password_hash=hash_password(data.password),
        logo=data.logo,
        comp_name=data.comp_name,
        rating=data.rating,
    )

    db.add(company)
    await db.commit()
    await db.refresh(company)
    return company


async def login_company(db: AsyncSession, username: str, password: str):
    result = await db.execute(
        select(TourCompanies).where(TourCompanies.username == username)
    )
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(401, "Invalid username or password")

    if not verify_password(password, company.password_hash):
        raise HTTPException(401, "Invalid username or password")

    access, refresh = create_tokens({"company_id": company.id})

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }


async def get_company(db: AsyncSession, company_id: int):
    result = await db.execute(
        select(TourCompanies).where(TourCompanies.id == company_id)
    )
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(404, "Company not found")

    return company


async def update_company(db: AsyncSession, company_id: int, data: TourCompanyUpdate):
    company = await get_company(db, company_id)

    payload = data.model_dump(exclude_unset=True)

    if "password" in payload:
        payload["password_hash"] = hash_password(payload.pop("password"))

    for key, value in payload.items():
        setattr(company, key, value)

    await db.commit()
    await db.refresh(company)
    return company



async def create_category(db: AsyncSession, current_company: TourCompanies, data: TourCategoryCreate):

    category = TourCategories(
        tour_company_id=current_company.id,
        title=data.title
    )

    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def get_category(db: AsyncSession, category_id: int, current_company: TourCompanies):

    result = await db.execute(
        select(TourCategories).where(
            TourCategories.id == category_id,
            TourCategories.tour_company_id == current_company.id,
        )
    )
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(404, "Category not found or no permission")

    return category


async def get_categories(db: AsyncSession, current_company: TourCompanies):

    result = await db.execute(
        select(TourCategories).where(
            TourCategories.tour_company_id == current_company.id
        )
    )
    return result.scalars().all()


async def update_category(db: AsyncSession, category_id: int, data: TourCategoryUpdate, current_company: TourCompanies):

    category = await get_category(db, category_id, current_company)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(category, key, value)

    await db.commit()
    await db.refresh(category)
    return category



async def create_guide(db: AsyncSession, current_company: TourCompanies, data: TourGuideCreate):

    guide = TourGuides(
        tour_company_id=current_company.id,
        name=data.name,
        surname=data.surname,
        about_self=data.about_self,
        rating=data.rating
    )

    db.add(guide)
    await db.commit()
    await db.refresh(guide)
    return guide


async def get_guide(db: AsyncSession, guide_id: int, current_company: TourCompanies):

    result = await db.execute(
        select(TourGuides).where(
            TourGuides.id == guide_id,
            TourGuides.tour_company_id == current_company.id
        )
    )
    guide = result.scalar_one_or_none()

    if not guide:
        raise HTTPException(404, "Guide not found or no permission")

    return guide


async def get_guides(db: AsyncSession, current_company: TourCompanies):

    result = await db.execute(
        select(TourGuides).where(
            TourGuides.tour_company_id == current_company.id
        )
    )
    return result.scalars().all()


async def update_guide(db: AsyncSession, guide_id: int, data: TourGuideUpdate, current_company: TourCompanies):

    guide = await get_guide(db, guide_id, current_company)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(guide, key, value)

    await db.commit()
    await db.refresh(guide)
    return guide




async def create_tour(db: AsyncSession, current_company: TourCompanies, data: TourCreate):

    category = await get_category(db, data.tour_category_id, current_company)
    guide = await get_guide(db, data.tour_guid_id, current_company)

    tour = Tours(
        tour_company_id=current_company.id,
        tour_category_id=category.id,
        tour_guid_id=guide.id,
        image=data.image,
        price=data.price,
        departure_date=data.departure_date,
        return_date=data.return_date,
        is_new=data.is_new,
        max_people=data.max_people,
        location=data.location
    )

    db.add(tour)
    await db.commit()
    await db.refresh(tour)
    return tour


async def get_tour(db: AsyncSession, tour_id: int, current_company: TourCompanies):

    result = await db.execute(
        select(Tours).where(
            Tours.id == tour_id,
            Tours.tour_company_id == current_company.id
        )
    )
    tour = result.scalar_one_or_none()

    if not tour:
        raise HTTPException(404, "Tour not found or no permission")

    return tour


async def get_tours(db: AsyncSession, current_company: TourCompanies):

    result = await db.execute(
        select(Tours).where(
            Tours.tour_company_id == current_company.id
        )
    )
    return result.scalars().all()


async def update_tour(db: AsyncSession, tour_id: int, data: TourUpdate, current_company: TourCompanies):

    tour = await get_tour(db, tour_id, current_company)
    payload = data.model_dump(exclude_unset=True)

    if "tour_category_id" in payload:
        await get_category(db, payload["tour_category_id"], current_company)

    if "tour_guid_id" in payload:
        await get_guide(db, payload["tour_guid_id"], current_company)

    for key, value in payload.items():
        setattr(tour, key, value)

    await db.commit()
    await db.refresh(tour)
    return tour


async def create_tour_file(
    db: AsyncSession,
    tour_id: int,
    data: TourFileCreate,
    company: TourCompanies
):
    await get_tour(db, tour_id, company)

    file = TourFiles(
        tour_id=tour_id,
        file_name=data.file_name
    )

    db.add(file)
    await db.commit()
    await db.refresh(file)
    return file



async def get_tour_files(
    db: AsyncSession,
    tour_id: int,
    company: TourCompanies
):
    await get_tour(db, tour_id, company)

    result = await db.execute(
        select(TourFiles).where(
            TourFiles.tour_id == tour_id
        )
    )
    return result.scalars().all()



async def delete_tour_file(
    db: AsyncSession,
    file_id: int,
    company: TourCompanies
):
    result = await db.execute(
        select(TourFiles).where(TourFiles.id == file_id)
    )
    file = result.scalar_one_or_none()

    if not file:
        raise HTTPException(404, "File not found")

    await get_tour(db, file.tour_id, company)

    await db.delete(file)
    await db.commit()

    return {"detail": "File deleted"}



def generate_secret_code() -> str:
    return "".join(random.choices(string.digits, k=6))


async def create_booking(db: AsyncSession, data: BookingCreate):
    secret = generate_secret_code()

    booking = BookingTour(
        tour_company_id=data.tour_company_id,
        tour_category_id=data.tour_category_id,
        tour_id=data.tour_id,
        person_number=data.person_number,
        name=data.name,
        surname=data.surname,
        patronymic=data.patronymic,
        phone=data.phone,
        email=data.email,
        passport_number=data.passport_number,
        date_of_birth=data.date_of_birth,
        booking_date=datetime.utcnow(),
        secret_code=secret
    )

    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    return booking