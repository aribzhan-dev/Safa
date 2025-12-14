from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sadaqa import HelpRequest
from app.schemas.sadaqa_schemas import (
    HelpRequestCreate,
    HelpRequestUpdate,
    HelpRequestOut
)
from app.core.db import get_session
from app.core.sadaqa_deps import get_current_sadaqa_company
from app.services.sadaqa_service import (
    create_help_request,
    get_help_requests,
    update_help_request
)

router = APIRouter(prefix="/sadaqa/company/help-requests")


@router.post("", response_model=HelpRequestOut)
async def create_my_help_request(
        data: HelpRequestCreate,
        db: AsyncSession = Depends(get_session),
        company=Depends(get_current_sadaqa_company)
):
    hr = HelpRequest(**data.model_dump())
    db.add(hr)
    await db.commit()
    await db.refresh(hr)

    return hr


@router.get("", response_model=list[HelpRequestOut])
async def list_my_help_requests(
        db: AsyncSession = Depends(get_session),
        company=Depends(get_current_sadaqa_company)
):
    return await get_help_requests(db, company)


@router.put("/{hr_id}", response_model=HelpRequestOut)
async def update_help_req(
        hr_id: int,
        data: HelpRequestUpdate,
        db: AsyncSession = Depends(get_session),
        company=Depends(get_current_sadaqa_company)
):
    return await update_help_request(db, hr_id, data, company)
