from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.sadaqa import MaterialsStatus, Company
from app.schemas.sadaqa_schemas import (
    MaterialsStatusCreate,
    MaterialsStatusUpdate
)

async def create_material_status(
    db: AsyncSession,
    data: MaterialsStatusCreate,
    company: Company
):
    ms = MaterialsStatus(
        company_id=company.id,
        **data.model_dump()
    )
    db.add(ms)
    await db.commit()
    await db.refresh(ms)
    return ms



async def get_material_statuses(
    db: AsyncSession,
    company: Company
):
    r = await db.execute(
        select(MaterialsStatus).where(
            MaterialsStatus.company_id == company.id
        )
    )
    return r.scalars().all()



async def update_material_status(
    db: AsyncSession,
    ms_id: int,
    data: MaterialsStatusUpdate,
    company: Company
):
    r = await db.execute(
        select(MaterialsStatus).where(
            MaterialsStatus.id == ms_id,
            MaterialsStatus.company_id == company.id
        )
    )
    ms = r.scalar_one_or_none()

    if not ms:
        raise HTTPException(404, "Material status not found")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(ms, k, v)

    await db.commit()
    await db.refresh(ms)
    return ms


