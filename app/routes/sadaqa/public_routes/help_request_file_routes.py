from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas.sadaqa_schemas import HelpRequestFileOut
from app.services.sadaqa_public.help_request_file_service import (
    create_help_request_file
)

router = APIRouter(
    prefix="/help-request-files",
    tags=["Sadaqa | HelpRequestFile (Public)"]
)


@router.post("/{help_request_id}", response_model=HelpRequestFileOut)
async def upload(
    help_request_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session)
):
    return await create_help_request_file(db, help_request_id, file)