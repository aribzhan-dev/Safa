from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.schemas.sadaqa_schemas import NoteCreate, NoteUpdate
from app.models.sadaqa import Note, Company, StatusEnum



async def create_note(
        db: AsyncSession,
        data: NoteCreate,
        company: Company
):
    if data.collected_money > data.goal_money:
        raise HTTPException(400, "Collected money cannot exceed goal")

    note = Note(
        company_id=company.id,
        status=StatusEnum.inactive,
        **data.model_dump(exclude="status")
    )
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def archive_active_note(
    db: AsyncSession,
    company_id: int
):
    stmt = (
        update(Note)
        .where(
            Note.company_id == company_id,
            Note.status == StatusEnum.active
        )
        .values(status=StatusEnum.archived)
    )
    await db.execute(stmt)


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
    result = await db.execute(
        select(Note).where(
            Note.id == note_id,
            Note.company_id == company.id
        )
    )
    note = result.scalar_one_or_none()

    if not note:
        raise HTTPException(404, "Note not found")

    payload = data.model_dump(exclude_unset=True)

    if payload.get("status") == StatusEnum.active:
        await archive_active_note(db, company.id)
        note.status = StatusEnum.active
        payload.pop("status", None)

    for k, v in payload.items():
        setattr(note, k, v)

    if note.collected_money > note.goal_money:
        raise HTTPException(400, "Collected money cannot exceed goal")

    try:
        await db.commit()
    except Exception:
        raise HTTPException(409, "Only one active note allowed")

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