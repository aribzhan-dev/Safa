from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sadaqa import MaterialsStatus


async def get_public_material_statuses(db: AsyncSession):
    r = await db.execute(
        select(
            MaterialsStatus.id,
            MaterialsStatus.title,
            MaterialsStatus.language_id
        )
        .where(MaterialsStatus.status == 0)
    )
    return r.all()