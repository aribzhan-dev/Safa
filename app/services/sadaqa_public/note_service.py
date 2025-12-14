from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sadaqa import Note

async def get_public_notes(db: AsyncSession):
    r = await db.execute(
        select(
            Note.id,
            Note.title,
            Note.content,
            Note.image,
            Note.goal_money,
            Note.collected_money,
            Note.language_id
        )
        .where(Note.status == 0)
    )
    return r.all()