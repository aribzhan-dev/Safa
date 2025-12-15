from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.sadaqa_deps import get_current_sadaqa_company
from app.schemas.sadaqa_schemas import HelpRequestOut, HelpRequestUpdate
from app.services.sadaqa_private.help_request_service import (
    get_company_help_requests,
    update_help_request
)

router = APIRouter(
    prefix="/help-requests",
    tags=["Sadaqa | HelpRequest (Company)"]
)


@router.get("/", response_model=list[HelpRequestOut],)
async def my_requests(
    db: AsyncSession = Depends(get_session),
    company=Depends(get_current_sadaqa_company)
):
    return await get_company_help_requests(db, company)


@router.put("/{hr_id}", response_model=HelpRequestOut)
async def update(
    hr_id: int,
    data: HelpRequestUpdate,
    db: AsyncSession = Depends(get_session),
    company=Depends(get_current_sadaqa_company)
):
    return await update_help_request(db, hr_id, data, company)