from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from app.models.sadaqa import Company, Post, StatusEnum


async def get_all_companies(db: AsyncSession):
    result = await db.execute(
        select(
            Company.id,
            Company.title,
            Company.why_collecting,
            Company.image,
            Company.payment,
            func.count(Post.id).label("post_count")
        )
        .outerjoin(
            Post,
            (Post.company_id == Company.id)
            & (Post.status == StatusEnum.active.name)
        )
        .group_by(Company.id)
    )

    return [
        {
            "id": row.id,
            "title": row.title,
            "why_collecting": row.why_collecting,
            "image": row.image,
            "payment": row.payment,
            "post_count": int(row.post_count or 0),
        }
        for row in result.all()
    ]


async def get_company_detail(db: AsyncSession, company_id: int):
    result = await db.execute(
        select(Company).where(Company.id == company_id)
    )
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(404, "Company not found")

    post_count = await db.scalar(
        select(func.count(Post.id))
        .where(
            Post.company_id == company.id,
            Post.status == StatusEnum.active
        )
    )

    return {
        "id": company.id,
        "title": company.title,
        "why_collecting": company.why_collecting,
        "image": company.image,
        "payment": company.payment,
        "post_count": int(post_count or 0),
    }