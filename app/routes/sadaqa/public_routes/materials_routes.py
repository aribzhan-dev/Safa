from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.services.sadaqa_public.material_status_service import (
    get_public_material_statuses
)

router = APIRouter(
    prefix="/materials-status",
    tags=["Sadaqa | MaterialsStatus (Public)"]
)


@router.get("/")
async def list_statuses(
    db: AsyncSession = Depends(get_session)
):
    return await get_public_material_statuses(db)