from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.services.tour_public.tour_service import get_public_tours

router = APIRouter(
    prefix="/tours",
    tags=["Tour / Tours (Public)"]
)

@router.get("/")
async def get_tours(
    db: AsyncSession = Depends(get_session)
):
    return await get_public_tours(db)