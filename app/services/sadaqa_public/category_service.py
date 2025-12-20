from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sadaqa import HelpCategory, StatusEnum


async def get_public_help_categories(
    db: AsyncSession,
    language_id: int | None = None
):
    query = select(
        HelpCategory.id,
        HelpCategory.title,
        HelpCategory.language_id,
        HelpCategory.is_other,
        HelpCategory.content,
    ).where(
        HelpCategory.status == StatusEnum.active
    )

    if language_id:
        query = query.where(HelpCategory.language_id == language_id)

    result = await db.execute(query)
    return result.mappings().all()