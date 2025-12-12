from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.sadaqa_schemas import (
    HelpRequestFileCreate, HelpRequestFileOut
)
from app.core.db import get_session
from app.core.sadaqa_deps import get_current_sadaqa_company
from app.services.sadaqa_service import create_help_request_file

router = APIRouter(prefix="/company/help-request/files")

@router.post("/", response_model=HelpRequestFileOut)
async def upload_help_file(
        data: HelpRequestFileCreate,
        db: AsyncSession = Depends(get_session),
        company=Depends(get_current_sadaqa_company)
):
    return await create_help_request_file(db, data, company)