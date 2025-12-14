from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.sadaqa_deps import get_current_sadaqa_company
from app.schemas.sadaqa_schemas import HelpRequestFileOut
from app.services.sadaqa_private.help_request_file_service import (
    get_files_by_company
)

router = APIRouter(
    prefix="/help-request-files",
    tags=["Sadaqa | HelpRequestFile (Company)"]
)


@router.get("/", response_model=list[HelpRequestFileOut])
async def my_files(
    db: AsyncSession = Depends(get_session),
    company=Depends(get_current_sadaqa_company)
):
    return await get_files_by_company(db, company)