from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.dependencies.admin_auth import get_current_admin
from app.services.admin.admin_service import create_language
from app.schemas.sadaqa_schemas import LanguageCreate

router = APIRouter(prefix="/languages")

@router.post("/")
async def create(
    data: LanguageCreate,
    db: AsyncSession = Depends(get_session),
    admin=Depends(get_current_admin)
):
    return await create_language(db, data)