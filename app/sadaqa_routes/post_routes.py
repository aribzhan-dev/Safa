from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.sadaqa_schemas import PostCreate, PostUpdate, PostOut
from app.core.db import get_session
from app.core.sadaqa_deps import get_current_sadaqa_company
from app.services.sadaqa_service import create_post, get_posts, update_post

router = APIRouter(prefix="/sadaqa/company/posts")

@router.post("", response_model=PostOut)
async def create_my_post(
        data: PostCreate,
        db: AsyncSession = Depends(get_session),
        company=Depends(get_current_sadaqa_company)
):
    return await create_post(db, data, company)


@router.get("", response_model=list[PostOut])
async def get_my_posts(
        db: AsyncSession = Depends(get_session),
        company=Depends(get_current_sadaqa_company)
):
    return await get_posts(db, company)


@router.put("/{post_id}", response_model=PostOut)
async def update_my_post(
        post_id: int,
        data: PostUpdate,
        db: AsyncSession = Depends(get_session),
        company=Depends(get_current_sadaqa_company)
):
    return await update_post(db, post_id, data, company)