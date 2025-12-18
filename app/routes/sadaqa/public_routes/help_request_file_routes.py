from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas.sadaqa_schemas import HelpRequestFileOut
from app.services.sadaqa_public.help_request_file_service import (
    create_help_request_file
)
from app.utils.file import upload_file

router = APIRouter(
    prefix="/help-request-files",
    tags=["Sadaqa | HelpRequestFile (Public)"]
)


@router.post("/{help_request_id}", response_model=HelpRequestFileOut)
async def upload_help_request_file(
    help_request_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session),
):
    file_path = await upload_file(file)
    return await create_help_request_file(
        db=db,
        help_request_id=help_request_id,
        file_path=file_path
    )