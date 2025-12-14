from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.services.sadaqa_public.post_service import get_public_posts

router = APIRouter(
    prefix="/posts",
    tags=["Sadaqa | Posts (Public)"]
)


@router.get("/")
async def list_posts(
    db: AsyncSession = Depends(get_session)
):
    return await get_public_posts(db)