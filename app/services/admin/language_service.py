from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sadaqa import Language



async def get_languages(db: AsyncSession):
    r = await db.execute(select(Language))
    return r.scalars().all()