from app.schemas.tour_schemas import TourCompanyCreate, TourCompanyUpdate, RefreshRequest
from app.services.tour_private.tour_company_service import update_company
from app.core.tour_deps import get_current_tour_company
from app.services.tour_private.tour_company_service import (
    # create_company,
    login_company,
    refresh_tokens,
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.core.db import get_session

router = APIRouter(
    prefix="/company",
    tags=["Tour / Company (Private)"]
)


# @router.post("/register")
# async def register_company(
#     data: TourCompanyCreate,
#     db: AsyncSession = Depends(get_session)
# ):
#     return await create_company(db, data)

@router.post("/login")
async def login(
    username: str,
    password: str,
    db: AsyncSession = Depends(get_session)
):
    return await login_company(db, username, password)


@router.post("/refresh")
async def refresh_token(data: RefreshRequest):
    return await refresh_tokens(data.refresh_token)


@router.put("/me")
async def update_my_company(
    data: TourCompanyUpdate,
    db: AsyncSession = Depends(get_session),
    company = Depends(get_current_tour_company)
):
    return await update_company(db, company, data)