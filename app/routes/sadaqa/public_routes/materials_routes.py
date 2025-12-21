from fastapi import APIRouter, Depends, Query
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
    company_id: int,
    language_id: int | None = Query(default=None),
    db: AsyncSession = Depends(get_session)
):
    return await get_public_material_statuses(
        db=db,
        company_id=company_id,
        language_id=language_id
    )