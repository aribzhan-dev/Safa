from fastapi import APIRouter
from app.routes.admin.auth_routes import router as auth_router
from app.routes.admin.company_routes import router as company_router
from app.routes.admin.language_routes import router as language_router
from app.routes.admin.notification_routes import router as notification_router

router = APIRouter(prefix="/admin", tags=["Admin"])

router.include_router(auth_router)
router.include_router(company_router)
router.include_router(language_router)
router.include_router(notification_router)