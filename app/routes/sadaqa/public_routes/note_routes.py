from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.sadaqa_schemas import NotePublicOut, NoteOut
from app.core.db import get_session
from app.services.sadaqa_public.note_service import get_public_active_note
from typing import Optional

router = APIRouter(
    prefix="/notes",
    tags=["Sadaqa | Notes (Public)"]
)


@router.get("/active", response_model=Optional[NotePublicOut])
async def get_active_note(
    company_id: int | None = None,
    db: AsyncSession = Depends(get_session),
):
    return await get_public_active_note(db, company_id)