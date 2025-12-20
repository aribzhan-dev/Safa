from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.db import get_session
from app.models.sadaqa import Company, Post
from app.schemas.sadaqa_schemas import CompanyPublicOut

router = APIRouter(
    prefix="/company",
    tags=["Sadaqa | Company (Public)"]
)


@router.get("/", response_model=list[CompanyPublicOut])
async def get_all_companies(
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(Company)
    )
    return result.scalars().all()


@router.get("/{company_id}", response_model=CompanyPublicOut)
async def get_company_detail(
    company_id: int,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(
        select(Company).where(Company.id == company_id)
    )
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(404, "Company not found")


    post_count_result = await db.execute(
        select(func.count(Post.id)).where(
            Post.company_id == company.id
        )
    )
    post_count = post_count_result.scalar() or 0

    return {
        **company.__dict__,
        "post_count": post_count
    }

