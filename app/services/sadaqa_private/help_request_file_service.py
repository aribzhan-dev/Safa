from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sadaqa import Company, HelpRequest
from app.models.sadaqa import HelpRequestFile

async def get_files_by_company(
    db: AsyncSession,
    company: Company
):
    r = await db.execute(
        select(HelpRequestFile)
        .join(HelpRequest)
        .where(HelpRequest.company_id == company.id)
    )
    return r.scalars().all()

