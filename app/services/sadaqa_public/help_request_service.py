from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.sadaqa import Company, HelpRequest, MaterialsStatus, HelpCategory
from app.schemas.sadaqa_schemas import HelpRequestCreate

async def create_help_request(db: AsyncSession, data: HelpRequestCreate):
    company = await db.scalar(select(Company).where(Company.id == data.company_id))
    if not company:
        raise HTTPException(400, "Invalid company_id")

    ms = await db.scalar(
        select(MaterialsStatus).where(
            MaterialsStatus.id == data.materials_status_id,
            MaterialsStatus.company_id == data.company_id,
        )
    )
    if not ms:
        raise HTTPException(400, "materials_status_id does not belong to selected company")

    cat = await db.scalar(
        select(HelpCategory).where(
            HelpCategory.id == data.help_category_id,
            HelpCategory.company_id == data.company_id,
        )
    )
    if not cat:
        raise HTTPException(400, "help_category_id does not belong to selected company")

    hr = HelpRequest(**data.model_dump())
    db.add(hr)
    await db.commit()
    await db.refresh(hr)
    return hr