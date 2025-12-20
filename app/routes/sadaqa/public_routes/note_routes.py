from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.sadaqa_schemas import NotePublicOut
from app.core.db import get_session
from app.services.sadaqa_public.note_service import get_public_active_note

router = APIRouter(
    prefix="/notes",
    tags=["Sadaqa | Notes (Public)"]
)


@router.get("/active", response_model=NotePublicOut | None)
async def get_active_note(
    company_id: int | None = None,
    language_id: int | None = None,
    db: AsyncSession = Depends(get_session),
):
    note = await get_public_active_note(db, company_id, language_id)

    if not note:
        return None

    return note