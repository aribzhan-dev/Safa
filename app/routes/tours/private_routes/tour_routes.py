from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.tour_deps import get_current_tour_company
from app.schemas.tour_schemas import TourCreate, TourUpdate
from app.services.tour_private.tour_service import (
    create_tour, get_tours, update_tour
)

router = APIRouter(
    prefix="/tours",
    tags=["Tour / Tours (Private)"]
)


@router.post("/")
async def create(
    data: TourCreate,
    db: AsyncSession = Depends(get_session),
    company = Depends(get_current_tour_company)
):
    return await create_tour(db, company, data)

@router.get("/")
async def list_(
    db: AsyncSession = Depends(get_session),
    company = Depends(get_current_tour_company)
):
    return await get_tours(db, company)

@router.put("/{tour_id}")
async def update(
    tour_id: int,
    data: TourUpdate,
    db: AsyncSession = Depends(get_session),
    company = Depends(get_current_tour_company)
):
    return await update_tour(db, tour_id, data, company)