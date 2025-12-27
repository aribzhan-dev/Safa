from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.dependencies.admin_auth import get_current_admin
from app.services.notification_service import notify_device
from app.schemas.notification_schemas import NotificationCreate

router = APIRouter(prefix="/notifications")

@router.post("/device")
async def send_to_device(
    data: NotificationCreate,
    db: AsyncSession = Depends(get_session),
    admin=Depends(get_current_admin)
):
    return await notify_device(db, data)