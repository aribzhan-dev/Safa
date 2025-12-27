from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.dependencies.admin_auth import get_current_admin
from app.services.admin.admin_service import (
    create_tour_company,
    create_sadaqa_company,
)

router = APIRouter(prefix="/companies")

@router.post("/tour")
async def create_tour(
    data,
    db: AsyncSession = Depends(get_session),
    admin=Depends(get_current_admin)
):
    return await create_tour_company(db, data)


@router.post("/sadaqa")
async def create_sadaqa(
    data,
    db: AsyncSession = Depends(get_session),
    admin=Depends(get_current_admin)
):
    return await create_sadaqa_company(db, data)