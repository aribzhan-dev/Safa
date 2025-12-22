from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas.tour_schemas import TourCompanyPublicOut, ActiveToursCountOut
from app.services.tour_public.company_service import get_public_companies, get_total_active_tours_count

router = APIRouter(
    prefix="/companies",
    tags=["Tour / Company (Public)"]
)

@router.get("/", response_model=list[TourCompanyPublicOut])
async def get_companies(
    db: AsyncSession = Depends(get_session)
):
    return await get_public_companies(db)


@router.get("/active-tours-count", summary="Get total active tours count", response_model=ActiveToursCountOut)
async def get_active_tours_count(
    db: AsyncSession = Depends(get_session)
):
    return {
        "active_tours_count": await get_total_active_tours_count(db)
    }