from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from app.models.sadaqa import HelpRequest
from app.models.sadaqa import Company, StatusEnum


async def get_company_help_requests(
    db: AsyncSession,
    company: Company
):
    result = await db.execute(
        select(HelpRequest)
        .where(HelpRequest.company_id == company.id)
    )
    return result.scalars().all()


async def update_help_request(
        db: AsyncSession,
        hr_id: int,
        status: StatusEnum,
        company: Company
):
    result = await db.execute(
        select(HelpRequest).where(
            HelpRequest.id == hr_id,
            HelpRequest.company_id == company.id
        )
    )
    hr = result.scalar_one_or_none()

    if not hr:
        raise HTTPException(404, "Help request not found or no permission")

    hr.status = status

    await db.commit()
    await db.refresh(hr)
    return hr