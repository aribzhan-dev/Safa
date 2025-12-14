from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas.sadaqa_schemas import HelpRequestCreate, HelpRequestOut
from app.services.sadaqa_public.help_request_service import create_help_request

router = APIRouter(
    prefix="/help-requests",
    tags=["Sadaqa | HelpRequest (Public)"]
)


@router.post("/", response_model=HelpRequestOut)
async def create(
    data: HelpRequestCreate,
    db: AsyncSession = Depends(get_session)
):
    return await create_help_request(db, data)