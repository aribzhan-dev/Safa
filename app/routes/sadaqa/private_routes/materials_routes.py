from http.client import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sadaqa import Company
from app.core.db import get_session
from app.core.sadaqa_deps import get_current_sadaqa_company
from app.schemas.sadaqa_schemas import (
    MaterialsStatusCreate,
    MaterialsStatusUpdate,
    MaterialsStatusOut
)
from app.services.sadaqa_private.material_status_service import (
    create_material_status,
    get_material_statuses,
    update_material_status,
    get_material_status_by_id,
    delete_material_status,
)

router = APIRouter(
    prefix="/materials-status",
    tags=["Sadaqa | MaterialsStatus (Private)"]
)
router.openapi_extra = {
    "security": [{"sadaqaAuth": []}]
}


@router.post("/", response_model=MaterialsStatusOut)
async def create(
    data: MaterialsStatusCreate,
    db: AsyncSession = Depends(get_session),
    company=Depends(get_current_sadaqa_company)
):
    return await create_material_status(db, data, company)


@router.get("/", response_model=list[MaterialsStatusOut])
async def list_my(
    db: AsyncSession = Depends(get_session),
    company=Depends(get_current_sadaqa_company)
):
    return await get_material_statuses(db, company)


@router.get("/{ms_id}", response_model=MaterialsStatusOut)
async def get_material_status(
    ms_id: int,
    db: AsyncSession = Depends(get_session),
    company=Depends(get_current_sadaqa_company)
):
    ms = await get_material_status_by_id(db, ms_id, company)

    if not ms:
        raise HTTPException(404, "Material status not found")

    return ms


@router.put("/{ms_id}", response_model=MaterialsStatusOut)
async def update(
    ms_id: int,
    data: MaterialsStatusUpdate,
    db: AsyncSession = Depends(get_session),
    company=Depends(get_current_sadaqa_company)
):
    return await update_material_status(db, ms_id, data, company)


@router.delete("/{ms_id}", response_model=MaterialsStatusOut)
async def delete_ms(
    ms_id: int,
    db: AsyncSession = Depends(get_session),
    company: Company = Depends(get_current_sadaqa_company)
):
    return await delete_material_status(db, ms_id, company)