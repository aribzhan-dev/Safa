from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.core.sadaqa_deps import get_current_sadaqa_company
from app.services.sadaqa_service import create_help_request_file

router = APIRouter(prefix="/sadaqa/company/help-requests", tags=["HelpRequestFile"])


@router.post("/{help_request_id}/files")
async def upload_help_request_file(
    help_request_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session),
    company = Depends(get_current_sadaqa_company)
):
    return await create_help_request_file(
        db=db,
        help_request_id=help_request_id,
        upload_file=file,
        company=company
    )