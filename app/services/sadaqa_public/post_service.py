from fastapi import  HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sadaqa import Post

async def get_public_posts(db: AsyncSession):
    r = await db.execute(
        select(
            Post.id,
            Post.title,
            Post.content,
            Post.image,
            Post.language_id
        )
        .where(Post.status == 0)
    )
    return r.all()