from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.services.admin.admin_service import admin_login
from app.schemas.admin_schemas import AdminLogin

router = APIRouter(prefix="/auth")

@router.post("/login")
async def login(
    data: AdminLogin,
    db: AsyncSession = Depends(get_session)
):
    return await admin_login(db, data.login, data.password)