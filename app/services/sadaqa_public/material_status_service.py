from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sadaqa import MaterialsStatus, StatusEnum


async def get_public_material_statuses(
    db: AsyncSession,
    company_id: int,
    language_id: int|None=None
):
    q = select(MaterialsStatus).where(
        MaterialsStatus.company_id == company_id,
        MaterialsStatus.status == StatusEnum.active
    )
    if language_id is not None:
        q = q.where(MaterialsStatus.language_id == language_id)

    res = await db.execute(q)
    return res.scalars().all()