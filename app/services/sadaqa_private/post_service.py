from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sadaqa import Post, Company
from app.schemas.sadaqa_schemas import PostCreate, PostUpdate



async def create_post(
        db: AsyncSession,
        data: PostCreate,
        company: Company
):
    post = Post(
        company_id=company.id,
        **data.model_dump()
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def get_posts(
        db: AsyncSession,
        company: Company
):
    r = await db.execute(
        select(Post).where(Post.company_id == company.id)
    )
    return r.scalars().all()


async def update_post(
        db: AsyncSession,
        post_id: int,
        data: PostUpdate,
        company: Company
):
    r = await db.execute(
        select(Post).where(
            Post.id == post_id,
            Post.company_id == company.id
        )
    )
    post = r.scalar_one_or_none()

    if not post:
        raise HTTPException(404, "Post not found or no permission")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(post, k, v)

    await db.commit()
    await db.refresh(post)
    return post


async def delete_post(
    db: AsyncSession,
    post_id: int,
    company: Company
):
    r = await db.execute(
        select(Post).where(
            Post.id == post_id,
            Post.company_id == company.id
        )
    )
    post = r.scalar_one_or_none()

    if not post:
        raise HTTPException(404, "Post not found or no permission")

    await db.delete(post)
    await db.commit()

    return {"detail": "Post deleted successfully"}