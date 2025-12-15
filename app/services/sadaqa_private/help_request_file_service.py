from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sadaqa import Company, HelpRequest

async def get_files_by_company(
    db: AsyncSession,
    company: Company
):
    r = await db.execute(
        select(HelpRequest)
        .options(selectinload(HelpRequest.files))
        .where(HelpRequest.company_id == company.id)
    )
    return r.scalars().all()

