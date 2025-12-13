from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.sadaqa_schemas import (
    HelpCategoryCreate,
    HelpCategoryUpdate,
    HelpCategoryOut
)
from app.core.db import get_session
from app.core.sadaqa_deps import get_current_sadaqa_company
from app.services.sadaqa_service import (
    create_help_category,
    get_help_categories,
    update_help_category
)

router = APIRouter(prefix="/sadaqa/company/categories")

@router.post("", response_model=HelpCategoryOut)
async def create_my_category(
        data: HelpCategoryCreate,
        db: AsyncSession = Depends(get_session),
        company=Depends(get_current_sadaqa_company)
):
    return await create_help_category(db, data, company)


@router.get("", response_model=list[HelpCategoryOut])
async def get_categories(
        db: AsyncSession = Depends(get_session),
        company=Depends(get_current_sadaqa_company)
):
    return await get_help_categories(db, company)



@router.put("/{cat_id}", response_model=HelpCategoryOut)
async def update_my_category(
        cat_id: int,
        data: HelpCategoryUpdate,
        db: AsyncSession = Depends(get_session),
        company=Depends(get_current_sadaqa_company)
):
    return await update_help_category(db, cat_id, data, company)