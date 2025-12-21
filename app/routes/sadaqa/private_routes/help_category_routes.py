from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.sadaqa_deps import get_current_sadaqa_company
from app.schemas.sadaqa_schemas import (
    HelpCategoryCreate,
    HelpCategoryUpdate,
    HelpCategoryOut
)
from app.services.sadaqa_private.category_service import (
    create_help_category,
    get_help_categories,
    update_help_category,
    get_help_category_by_id,
    delete_help_category,
)

router = APIRouter(
    prefix="/help-categories",
    tags=["Sadaqa | HelpCategory (Private)"]
)
router.openapi_extra = {
    "security": [{"sadaqaAuth": []}]
}


@router.post("/", response_model=HelpCategoryOut)
async def create(
    data: HelpCategoryCreate,
    db: AsyncSession = Depends(get_session),
    company=Depends(get_current_sadaqa_company)
):
    return await create_help_category(db, data, company)


@router.get("/", response_model=list[HelpCategoryOut])
async def my_categories(
    db: AsyncSession = Depends(get_session),
    company=Depends(get_current_sadaqa_company)
):
    return await get_help_categories(db, company)


@router.get("/{category_id}", response_model=HelpCategoryOut)
async def get_help_category(
    category_id: int,
    db: AsyncSession = Depends(get_session),
    company=Depends(get_current_sadaqa_company)
):
    category = await get_help_category_by_id(db, category_id, company)

    if not category:
        raise HTTPException(404, "Help category not found")

    return category


@router.put("/{category_id}", response_model=HelpCategoryOut)
async def update(
    category_id: int,
    data: HelpCategoryUpdate,
    db: AsyncSession = Depends(get_session),
    company=Depends(get_current_sadaqa_company)
):
    return await update_help_category(db, category_id, data, company)


@router.delete("/{category_id}", response_model=HelpCategoryOut)
async def delete_help_cat(
    category_id: int,
    db: AsyncSession = Depends(get_session),
    company=Depends(get_current_sadaqa_company)
):
    return await delete_help_category(db, category_id, company)