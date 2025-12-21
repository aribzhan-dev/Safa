from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.tour_deps import get_current_tour_company
from app.schemas.tour_schemas import TourCategoryCreate, TourCategoryUpdate
from app.services.tour_private.tour_category_service import (
    create_category, get_categories, update_category
)

router = APIRouter(
    prefix="/categories",
    tags=["Tour / Categories (Private)"]
)
router.openapi_extra = {
    "security": [{"sadaqaAuth": []}]
}

@router.post("/")
async def create(
    data: TourCategoryCreate,
    db: AsyncSession = Depends(get_session),
    company = Depends(get_current_tour_company)
):
    return await create_category(db, company, data)

@router.get("/")
async def list_(
    db: AsyncSession = Depends(get_session),
    company = Depends(get_current_tour_company)
):
    return await get_categories(db, company)

@router.put("/{category_id}")
async def update(
    category_id: int,
    data: TourCategoryUpdate,
    db: AsyncSession = Depends(get_session),
    company = Depends(get_current_tour_company)
):
    return await update_category(db, category_id, data, company)