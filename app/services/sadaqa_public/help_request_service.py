from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.sadaqa import (
    HelpRequest,
    MaterialsStatus,
    HelpCategory
)
from app.schemas.sadaqa_schemas import HelpRequestCreate


async def create_help_request(
    db: AsyncSession,
    data: HelpRequestCreate
):
    r = await db.execute(
        select(MaterialsStatus).where(
            MaterialsStatus.id == data.materials_status_id
        )
    )
    ms = r.scalar_one_or_none()

    if not ms:
        raise HTTPException(400, "Invalid materials_status_id")

    company_id = ms.company_id

    r = await db.execute(
        select(HelpCategory).where(
            HelpCategory.id == data.help_category_id,
            HelpCategory.company_id == company_id
        )
    )
    if not r.scalar_one_or_none():
        raise HTTPException(400, "Category does not belong to this company")

    hr = HelpRequest(
        company_id=company_id,
        **data.model_dump()
    )

    db.add(hr)
    await db.commit()
    await db.refresh(hr)
    return hr