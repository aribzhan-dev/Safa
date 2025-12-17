from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.services.tour_public.company_service import get_public_companies

router = APIRouter(
    prefix="/companies",
    tags=["Tour / Company (Public)"]
)

@router.get("/")
async def get_companies(
    db: AsyncSession = Depends(get_session)
):
    return await get_public_companies(db)