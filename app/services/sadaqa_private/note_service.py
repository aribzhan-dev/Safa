from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.sadaqa_schemas import NoteCreate, NoteUpdate
from app.models.sadaqa import Note, Company



async def create_note(
        db: AsyncSession,
        data: NoteCreate,
        company: Company
):
    if data.collected_money > data.goal_money:
        raise HTTPException(400, "Collected money cannot exceed goal")

    note = Note(company_id=company.id, **data.model_dump())
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def get_notes(
        db: AsyncSession,
        company: Company
):
    r = await db.execute(
        select(Note).where(Note.company_id == company.id)
    )
    return r.scalars().all()


async def update_note(
        db: AsyncSession,
        note_id: int,
        data: NoteUpdate,
        company: Company
):
    r = await db.execute(
        select(Note).where(
            Note.id == note_id,
            Note.company_id == company.id
        )
    )
    note = r.scalar_one_or_none()

    if not note:
        raise HTTPException(404, "Note not found or no permission")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(note, k, v)

    if note.collected_money > note.goal_money:
        raise HTTPException(400, "Collected money cannot exceed goal")

    await db.commit()
    await db.refresh(note)
    return note


async def delete_note(
    db: AsyncSession,
    note_id: int,
    company: Company
):
    r = await db.execute(
        select(Note).where(
            Note.id == note_id,
            Note.company_id == company.id
        )
    )
    note = r.scalar_one_or_none()

    if not note:
        raise HTTPException(404, "Note not found or no permission")

    await db.delete(note)
    await db.commit()

    return {"detail": "Note deleted successfully"}