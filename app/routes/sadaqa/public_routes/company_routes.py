from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas.sadaqa_schemas import CompanyPublicOut
from app.services.sadaqa_public.company_service import (
    get_all_companies,
    get_company_detail
)

router = APIRouter(
    prefix="/company",
    tags=["Sadaqa | Company (Public)"]
)


@router.get("/", response_model=list[CompanyPublicOut])
async def get_all_companies_route(
    db: AsyncSession = Depends(get_session)
):
    return await get_all_companies(db)


@router.get("/{company_id}", response_model=CompanyPublicOut)
async def company_detail(
    company_id: int,
    db: AsyncSession = Depends(get_session)
):
    return await get_company_detail(db, company_id)