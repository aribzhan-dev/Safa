from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.services.sadaqa_public.category_service import (
    get_public_company_categories
)
from app.schemas.sadaqa_schemas import HelpCategoryPublicOut


router = APIRouter(
    prefix="/categories",
    tags=["Sadaqa / Public / Categories"]
)


@router.get(
    "/",
    response_model=list[HelpCategoryPublicOut],
    summary="Get public help categories"
)
async def get_categories(
    company_id: int,
    language_id: int | None = Query(default=None),
    db: AsyncSession = Depends(get_session)
):
    return await get_public_company_categories(
        db=db,
        company_id=company_id,
        language_id=language_id
    )