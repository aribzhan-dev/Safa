from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.sadaqa_deps import get_current_sadaqa_company

from app.schemas.sadaqa_schemas import (
    CompanyCreate, CompanyLogin, CompanyUpdate,
    CompanyOut, TokenResponse
)

from app.services.sadaqa_service import (
    create_company, login_company, update_company
)

router = APIRouter(
    prefix="/sadaqa/company",
    tags=["Company"]
)


@router.post("/create", response_model=TokenResponse)
async def register_company(
    data: CompanyCreate,
    db: AsyncSession = Depends(get_session)
):
    return await create_company(db, data)


@router.post("/login", response_model=TokenResponse)
async def login(
    data: CompanyLogin,
    db: AsyncSession = Depends(get_session)
):
    return await login_company(db, data.login, data.password)



@router.put(
    "/me",
    response_model=CompanyOut,
    dependencies=[Depends(get_current_sadaqa_company)]
)
async def update_my_company(
    data: CompanyUpdate,
    db: AsyncSession = Depends(get_session),
    company=Depends(get_current_sadaqa_company)
):
    return await update_company(db, company.id, data)