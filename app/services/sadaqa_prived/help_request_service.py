from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.sadaqa import HelpRequest
from app.schemas.sadaqa_schemas import HelpRequestUpdate
from app.models.sadaqa import Company

async def get_company_help_requests(
    db: AsyncSession,
    company: Company
):
    r = await db.execute(
        select(HelpRequest).where(
            HelpRequest.company_id == company.id
        )
    )
    return r.scalars().all()


async def update_help_request(
    db: AsyncSession,
    hr_id: int,
    data: HelpRequestUpdate,
    company: Company
):
    r = await db.execute(
        select(HelpRequest).where(
            HelpRequest.id == hr_id,
            HelpRequest.company_id == company.id
        )
    )
    hr = r.scalar_one_or_none()

    if not hr:
        raise HTTPException(404, "HelpRequest not found or no permission")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(hr, k, v)

    await db.commit()
    await db.refresh(hr)
    return hr