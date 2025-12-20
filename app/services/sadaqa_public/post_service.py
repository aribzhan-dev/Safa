from fastapi import  HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sadaqa import Post, StatusEnum

async def get_public_posts(db: AsyncSession):
    r = await db.execute(
        select(
            Post.id,
            Post.company_id,
            Post.title,
            Post.content,
            Post.image,
            Post.language_id
        ).where(Post.status == StatusEnum.active)
    )
    return r.mappings().all()