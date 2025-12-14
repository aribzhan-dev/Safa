from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.sadaqa import HelpRequest
from app.schemas.sadaqa_schemas import HelpRequestCreate

async def create_help_request(
    db: AsyncSession,
    data: HelpRequestCreate
):
    hr = HelpRequest(**data.model_dump())
    db.add(hr)
    await db.commit()
    await db.refresh(hr)
    return hr


async def get_company_help_requests(
    db: AsyncSession,
    company_id: int
):
    r = await db.execute(
        select(HelpRequest).where(
            HelpRequest.company_id == company_id
        )
    )
    return r.scalars().all()