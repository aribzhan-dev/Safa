from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.sadaqa_schemas import (
    MaterialsStatusCreate,
    MaterialsStatusUpdate,
    MaterialsStatusOut
)
from app.core.db import get_session
from app.core.sadaqa_deps import get_current_sadaqa_company
from app.services.sadaqa_service import (
    create_material_status,
    get_material_statuses,
    update_material_status
)

router = APIRouter(prefix="/company/materials")


@router.post("", response_model=MaterialsStatusOut)
async def create_my_material_status(
        data: MaterialsStatusCreate,
        db: AsyncSession = Depends(get_session),
        company=Depends(get_current_sadaqa_company)
):
    return await create_material_status(db, data, company)


@router.get("", response_model=list[MaterialsStatusOut])
async def get_my_materials(
        db: AsyncSession = Depends(get_session),
        company=Depends(get_current_sadaqa_company)
):
    return await get_material_statuses(db, company)


@router.put("/{ms_id}", response_model=MaterialsStatusOut)
async def update_my_material(
        ms_id: int, data: MaterialsStatusUpdate,
        db: AsyncSession = Depends(get_session),
        company=Depends(get_current_sadaqa_company)
):
    return await update_material_status(db, ms_id, data, company)