from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.services.admin.language_service import get_languages
from app.schemas.sadaqa_schemas import LanguageOut


router = APIRouter(
    prefix="/languages",
    tags=["Sadaqa / Public / Languages"]
)


@router.get(
    "/",
    response_model=list[LanguageOut],
    summary="Get available languages"
)
async def list_languages(
    db: AsyncSession = Depends(get_session)
):
    return await get_languages(db)