from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.services.tour_public.guide_service import get_public_guides

router = APIRouter(
    prefix="/guides",
    tags=["Tour / Guides (Public)"]
)

@router.get("/")
async def get_guides(
    db: AsyncSession = Depends(get_session)
):
    return await get_public_guides(db)