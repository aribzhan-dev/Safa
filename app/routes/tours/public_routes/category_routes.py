from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.services.tour_public.tour_category_service import get_public_categories

router = APIRouter(
    prefix="/categories",
    tags=["Tour / Categories (Public)"]
)

@router.get("/")
async def get_categories(
    db: AsyncSession = Depends(get_session)
):
    return await get_public_categories(db)