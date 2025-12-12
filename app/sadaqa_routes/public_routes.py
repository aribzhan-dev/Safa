from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.schemas.sadaqa_schemas import HelpRequestCreate, HelpRequestOut
from app.services.sadaqa_service import public_create_help_request

router = APIRouter(prefix="/sadaqa/public", tags=["Public"])

@router.post("/help-requests", response_model=HelpRequestOut)
async def send_help_request(
    data: HelpRequestCreate,
    db: AsyncSession = Depends(get_session)
):
    return await public_create_help_request(db, data)