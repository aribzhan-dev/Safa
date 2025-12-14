from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.services.sadaqa_public.note_service import get_public_notes

router = APIRouter(
    prefix="/notes",
    tags=["Sadaqa | Notes (Public)"]
)


@router.get("/")
async def list_notes(
    db: AsyncSession = Depends(get_session)
):
    return await get_public_notes(db)