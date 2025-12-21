from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sadaqa import Company, Post
from app.core.db import get_session
from app.core.sadaqa_deps import get_current_sadaqa_company
from app.schemas.sadaqa_schemas import PostCreate, PostUpdate, PostOut
from app.services.sadaqa_private.post_service import (
    create_post, get_posts, update_post,
    delete_post
)

router = APIRouter(
    prefix="/posts",
    tags=["Sadaqa | Post (Private)"]
)
router.openapi_extra = {
    "security": [{"sadaqaAuth": []}]
}


@router.post("/", response_model=PostOut)
async def create(
    data: PostCreate,
    db: AsyncSession = Depends(get_session),
    company=Depends(get_current_sadaqa_company)
):
    return await create_post(db, data, company)


@router.get("/", response_model=list[PostOut])
async def my_posts(
    db: AsyncSession = Depends(get_session),
    company=Depends(get_current_sadaqa_company)
):
    return await get_posts(db, company)


@router.put("/{post_id}", response_model=PostOut)
async def update(
    post_id: int,
    data: PostUpdate,
    db: AsyncSession = Depends(get_session),
    company=Depends(get_current_sadaqa_company)
):
    return await update_post(db, post_id, data, company)


@router.delete("/{post_id}", response_model=PostOut)
async def delete(
    post_id: int,
    db: AsyncSession = Depends(get_session),
    company: Company = Depends(get_current_sadaqa_company)
):
    return await delete_post(db, post_id, company)