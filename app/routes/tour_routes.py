from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas.tour_schemas import (
    TourCompanyCreate, TourCompanyUpdate,
    TourCategoryCreate, TourCategoryUpdate,
    TourGuideCreate, TourGuideUpdate,
    TourCreate, TourUpdate,
)
from app.services.tour_service import (
    create_company, login_company, get_company, update_company,
    create_category, get_category, get_categories, update_category,
    create_guide, get_guide, get_guides, update_guide,
    create_tour, get_tour, get_tours, update_tour
)
from app.core.deps import get_current_company


router = APIRouter(prefix="/tour", tags=["Tour System"])



@router.post("/company", summary="Create Tour Company")
async def register_company(data: TourCompanyCreate, db: AsyncSession = Depends(get_session)):
    return await create_company(db, data)



@router.post("/auth/login", summary="Login company (JWT)")
async def login(data: dict, db: AsyncSession = Depends(get_session)):
    if "username" not in data or "password" not in data:
        raise HTTPException(400, "username and password are required")

    return await login_company(db, data["username"], data["password"])



@router.get("/company/me", summary="Get current company info")
async def get_my_company(
    db: AsyncSession = Depends(get_session),
    current_company = Depends(get_current_company)
):
    return await get_company(db, current_company.id)



@router.patch("/company/me", summary="Update current company")
async def update_my_company(
    data: TourCompanyUpdate,
    db: AsyncSession = Depends(get_session),
    current_company = Depends(get_current_company)
):
    return await update_company(db, current_company.id, data)




@router.post("/categories", summary="Create category")
async def create_cat(
    data: TourCategoryCreate,
    db: AsyncSession = Depends(get_session),
    current_company = Depends(get_current_company)
):
    return await create_category(db, current_company, data)


@router.get("/categories", summary="List categories")
async def list_categories(
    db: AsyncSession = Depends(get_session),
    current_company = Depends(get_current_company)
):
    return await get_categories(db, current_company)


@router.get("/categories/{cat_id}", summary="Get category")
async def get_cat(
    cat_id: int,
    db: AsyncSession = Depends(get_session),
    current_company = Depends(get_current_company)
):
    return await get_category(db, cat_id, current_company)



@router.patch("/categories/{cat_id}", summary="Update category")
async def patch_cat(
    cat_id: int,
    data: TourCategoryUpdate,
    db: AsyncSession = Depends(get_session),
    current_company = Depends(get_current_company)
):
    return await update_category(db, cat_id, data, current_company)




@router.post("/guides", summary="Create guide")
async def create_new_guide(
    data: TourGuideCreate,
    db: AsyncSession = Depends(get_session),
    current_company = Depends(get_current_company)
):
    return await create_guide(db, current_company, data)


@router.get("/guides", summary="List guides")
async def list_guides(
    db: AsyncSession = Depends(get_session),
    current_company = Depends(get_current_company)
):
    return await get_guides(db, current_company)



@router.get("/guides/{guide_id}", summary="Get guide")
async def get_one_guide(
    guide_id: int,
    db: AsyncSession = Depends(get_session),
    current_company = Depends(get_current_company)
):
    return await get_guide(db, guide_id, current_company)


@router.patch("/guides/{guide_id}", summary="Update guide")
async def patch_guide(
    guide_id: int,
    data: TourGuideUpdate,
    db: AsyncSession = Depends(get_session),
    current_company = Depends(get_current_company)
):
    return await update_guide(db, guide_id, data, current_company)



@router.post("/tours", summary="Create tour")
async def create_new_tour(
    data: TourCreate,
    db: AsyncSession = Depends(get_session),
    current_company = Depends(get_current_company)
):
    return await create_tour(db, current_company, data)



@router.get("/tours", summary="List tours")
async def list_tours(
    db: AsyncSession = Depends(get_session),
    current_company = Depends(get_current_company)
):
    return await get_tours(db, current_company)



@router.get("/tours/{tour_id}", summary="Get tour")
async def get_one_tour(
    tour_id: int,
    db: AsyncSession = Depends(get_session),
    current_company = Depends(get_current_company)
):
    return await get_tour(db, tour_id, current_company)



@router.patch("/tours/{tour_id}", summary="Update tour")
async def patch_tour(
    tour_id: int,
    data: TourUpdate,
    db: AsyncSession = Depends(get_session),
    current_company = Depends(get_current_company)
):
    return await update_tour(db, tour_id, data, current_company)