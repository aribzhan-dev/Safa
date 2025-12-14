from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sadaqa import HelpCategory, Company
from app.schemas.sadaqa_schemas import HelpCategoryCreate, HelpCategoryUpdate



async def create_help_category(
        db: AsyncSession,
        data: HelpCategoryCreate,
        company: Company
):
    cat = HelpCategory(
        company_id=company.id,
        **data.model_dump()
    )
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return cat


async def get_help_categories(
        db: AsyncSession,
        company: Company
):
    r = await db.execute(
        select(HelpCategory).where(HelpCategory.company_id == company.id)
    )
    return r.scalars().all()


async def update_help_category(
    db: AsyncSession,
    category_id: int,
    data: HelpCategoryUpdate,
    company: Company
):
    result = await db.execute(
        select(HelpCategory).where(
            HelpCategory.id == category_id,
            HelpCategory.company_id == company.id
        )
    )
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Help category not found or no permission"
        )

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(category, key, value)

    await db.commit()
    await db.refresh(category)

    return category