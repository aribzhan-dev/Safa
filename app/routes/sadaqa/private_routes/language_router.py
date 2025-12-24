from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas.sadaqa_schemas import LanguageCreate, LanguageOut
from app.services.admin.admin_service import create_language


router = APIRouter(
    prefix="/languages",
    tags=["Sadaqa / Private / Languages"]
)


@router.post(
    "/",
    response_model=LanguageOut,
    summary="Create language (admin)"
)
async def add_language(
    data: LanguageCreate,
    db: AsyncSession = Depends(get_session)
):
    return await create_language(db, data)