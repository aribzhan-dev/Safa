from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.sadaqa import (
    HelpRequest,
    MaterialsStatus,
    HelpCategory
)
from app.schemas.sadaqa_schemas import HelpRequestCreate


from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sadaqa import HelpRequest, MaterialsStatus, HelpCategory, StatusEnum
from app.schemas.sadaqa_schemas import HelpRequestCreate


async def create_help_request(
    db: AsyncSession,
    data: HelpRequestCreate
):
    r = await db.execute(
        select(MaterialsStatus).where(
            MaterialsStatus.id == data.materials_status_id,
            MaterialsStatus.company_id == data.company_id
        )
    )
    if not r.scalar_one_or_none():
        raise HTTPException(400, "Invalid materials_status_id for this company")

    r = await db.execute(
        select(HelpCategory).where(
            HelpCategory.id == data.help_category_id,
            HelpCategory.company_id == data.company_id
        )
    )
    if not r.scalar_one_or_none():
        raise HTTPException(400, "Category does not belong to this company")

    hr = HelpRequest(
        company_id=data.company_id,
        status=StatusEnum.inactive,
        **data.model_dump(exclude={"company_id"})
    )

    db.add(hr)
    await db.commit()
    await db.refresh(hr)
    return hr