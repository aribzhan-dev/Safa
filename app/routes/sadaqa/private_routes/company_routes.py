from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.core.sadaqa_deps import get_current_sadaqa_company
from app.schemas.sadaqa_schemas import (
    CompanyCreate,
    CompanyLogin,
    CompanyUpdate,
    CompanyOut,
    RefreshRequest,
    TokenResponse
)
from app.services.sadaqa_private.company_service import (
    create_company,
    login_company,
    update_company,
    refresh_tokens,
    logout,
)

router = APIRouter(
    prefix="/company",
    tags=["Sadaqa | Company (Private)"]
)
router.openapi_extra = {
    "security": [{"sadaqaAuth": []}]
}


@router.post("/register", response_model=TokenResponse)
async def register_company(
    data: CompanyCreate,
    db: AsyncSession = Depends(get_session)
):
    return await create_company(db, data)


@router.post("/login", response_model=TokenResponse)
async def login_company_route(
    data: CompanyLogin,
    db: AsyncSession = Depends(get_session)
):
    return await login_company(db, data.login, data.password)




@router.post("/refresh")
async def refresh_token(data: RefreshRequest):
    return await refresh_tokens(data.refresh_token)


@router.post("/logout")
async def logout_route(data: RefreshRequest):
    return await logout(data.refresh_token)




@router.put("/me", response_model=CompanyOut)
async def update_my_company(
    data: CompanyUpdate,
    db: AsyncSession = Depends(get_session),
    company=Depends(get_current_sadaqa_company)
):
    return await update_company(db, company.id, data)