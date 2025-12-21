from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sadaqa import HelpCategory, StatusEnum


async def get_public_company_categories(
    db: AsyncSession,
    company_id: int,
    language_id: int|None=None
):
    q = select(HelpCategory).where(
        HelpCategory.company_id == company_id,
        HelpCategory.status == StatusEnum.active
    )
    if language_id is not None:
        q = q.where(HelpCategory.language_id == language_id)

    res = await db.execute(q)
    return res.scalars().all()