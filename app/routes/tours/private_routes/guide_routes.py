from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.tour_deps import get_current_tour_company
from app.schemas.tour_schemas import TourGuideCreate, TourGuideUpdate
from app.services.tour_private.guide_service import (
    create_guide, get_guides, update_guide
)

router = APIRouter(
    prefix="/guides",
    tags=["Tour / Guides (Private)"]
)
router.openapi_extra = {
    "security": [{"sadaqaAuth": []}]
}

@router.post("/")
async def create(
    data: TourGuideCreate,
    db: AsyncSession = Depends(get_session),
    company = Depends(get_current_tour_company)
):
    return await create_guide(db, company, data)

@router.get("/")
async def list_guides(
    db: AsyncSession = Depends(get_session),
    company = Depends(get_current_tour_company)
):
    return await get_guides(db, company)

@router.put("/{guide_id}")
async def update(
    guide_id: int,
    data: TourGuideUpdate,
    db: AsyncSession = Depends(get_session),
    company = Depends(get_current_tour_company)
):
    return await update_guide(db, guide_id, data, company)