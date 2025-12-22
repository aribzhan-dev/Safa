from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.sadaqa import Company, HelpRequest, MaterialsStatus, HelpCategory
from app.schemas.sadaqa_schemas import HelpRequestCreate
from app.services.notification_service import notify_sadaqa_company


async def create_help_request(
    db: AsyncSession,
    data: HelpRequestCreate
):
    company = await db.scalar(
        select(Company).where(Company.id == data.company_id)
    )
    if not company:
        raise HTTPException(400, "Invalid company_id")

    ms = await db.scalar(
        select(MaterialsStatus).where(
            MaterialsStatus.id == data.materials_status_id,
            MaterialsStatus.company_id == data.company_id,
        )
    )
    if not ms:
        raise HTTPException(
            400,
            "materials_status_id does not belong to selected company"
        )

    cat = await db.scalar(
        select(HelpCategory).where(
            HelpCategory.id == data.help_category_id,
            HelpCategory.company_id == data.company_id,
        )
    )
    if not cat:
        raise HTTPException(
            400,
            "help_category_id does not belong to selected company"
        )

    hr = HelpRequest(
        company_id=data.company_id,
        materials_status_id=data.materials_status_id,
        help_category_id=data.help_category_id,
        name=data.name,
        surname=data.surname,
        age=data.age,
        phone_number=data.phone_number,
        other_category=data.other_category,
        child_num=data.child_num,
        address=data.address,
        iin=data.iin,
        help_reason=data.help_reason,
        received_other_help=data.received_other_help,
    )

    db.add(hr)
    await db.commit()
    await db.refresh(hr)

    await notify_sadaqa_company(
        db=db,
        company_id=company.id,
        title="New Help Request",
        body=f"{data.name} {data.surname} asked help request",
        type_="help_request",
    )

    return hr