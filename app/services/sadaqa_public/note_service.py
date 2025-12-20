from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sadaqa import Note, StatusEnum

async def get_public_active_note(
    db: AsyncSession,
    company_id: int | None = None,
    language_id: int | None = None,
):
    query = select(Note).where(Note.status == StatusEnum.active)

    if company_id:
        query = query.where(Note.company_id == company_id)

    if language_id:
        query = query.where(Note.language_id == language_id)

    result = await db.execute(query)
    return result.scalar_one_or_none()