from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sadaqa import HelpRequest, HelpRequestFile, Company


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