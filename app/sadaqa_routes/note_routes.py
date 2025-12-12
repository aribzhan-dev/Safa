from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.sadaqa_schemas import NoteCreate, NoteUpdate, NoteOut
from app.core.db import get_session
from app.core.sadaqa_deps import get_current_sadaqa_company
from app.services.sadaqa_service import create_note, get_notes, update_note

router = APIRouter(prefix="/company/notes")


@router.post("", response_model=NoteOut)
async def create_my_note(
        data: NoteCreate,
        db: AsyncSession = Depends(get_session),
        company=Depends(get_current_sadaqa_company)
):
    return await create_note(db, data, company)


@router.get("", response_model=list[NoteOut])
async def get_my_notes(
        db: AsyncSession = Depends(get_session),
        company=Depends(get_current_sadaqa_company)
):
    return await get_notes(db, company)


@router.put("/{note_id}", response_model=NoteOut)
async def update_my_note(
        note_id: int, data: NoteUpdate,
        db: AsyncSession = Depends(get_session),
        company=Depends(get_current_sadaqa_company)
):
    return await update_note(db, note_id, data, company)