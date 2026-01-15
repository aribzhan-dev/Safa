from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas.admin_schemas import AdminLogin
from app.schemas.tour_schemas import TourCompanyCreate
from app.schemas.sadaqa_schemas import CompanyCreate, LanguageCreate

from app.services.admin.admin_service import (
    admin_login,
    create_tour_company,
    create_sadaqa_company,
    create_language,
)

from app.dependencies.admin_auth import get_current_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.post("/login")
async def login_admin(
    data: AdminLogin,
    db: AsyncSession = Depends(get_session)
):
    return await admin_login(
        db=db,
        login=data.login,
        password=data.password
    )



@router.post(
    "/tour-companies",
    dependencies=[Depends(get_current_admin)]
)
async def admin_create_tour_company(
    data: TourCompanyCreate,
    db: AsyncSession = Depends(get_session),
):
    return await create_tour_company(db, data)




@router.post(
    "/sadaqa-companies",
    dependencies=[Depends(get_current_admin)]
)
async def admin_create_sadaqa_company(
    data: CompanyCreate,
    db: AsyncSession = Depends(get_session),
):
    return await create_sadaqa_company(db, data)



@router.post(
    "/languages",
    dependencies=[Depends(get_current_admin)]
)
async def admin_create_language(
    data: LanguageCreate,
    db: AsyncSession = Depends(get_session),
):
    return await create_language(db, data)