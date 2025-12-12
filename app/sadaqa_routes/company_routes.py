from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.sadaqa_deps import get_current_sadaqa_company
from app.core.db import get_session
from app.schemas.sadaqa_schemas import CompanyCreate, CompanyLogin, CompanyUpdate, CompanyOut, TokenResponse
from app.services.sadaqa_service import create_company, login_company, update_company
from app.core.jwt import decode_refresh_token, create_tokens

router = APIRouter(prefix="/company")

@router.post("/create", response_model=TokenResponse)
async def register_company(data: CompanyCreate, db: AsyncSession = Depends(get_session)):
    return await create_company(db, data)


@router.post("/login")
async def login(data: CompanyLogin, db: AsyncSession = Depends(get_session)):
    return await login_company(db, data.login, data.password)


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    payload = decode_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(401, "Invalid refresh token")

    access, refresh = create_tokens({"company_id": payload["company_id"]})
    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "Bearer"
    }


@router.put("/me", response_model=CompanyOut)
async def update_my_company(
        data: CompanyUpdate,
        db: AsyncSession = Depends(get_session),
        company=Depends(get_current_sadaqa_company)
):
    return await update_company(db, company.id, data)