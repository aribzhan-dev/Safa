from fastapi import APIRouter
from app.routes.sadaqa.public_routes.post_routes import router as post_router
from app.routes.sadaqa.public_routes.note_routes import router as note_router
from app.routes.sadaqa.public_routes.materials_routes import router as materials_router
from app.routes.sadaqa.public_routes.help_request_routes import router as help_request_router
from app.routes.sadaqa.public_routes.help_request_file_routes import router as help_request_file_router
from app.routes.sadaqa.public_routes.company_routes import router as company_router
from app.routes.sadaqa.public_routes.help_category_routes import router as help_category_router
from app.routes.sadaqa.public_routes.language_routes import router as language_router

router = APIRouter(
    tags=["Sadaqa | Public"]
)

router.include_router(post_router)
router.include_router(note_router)
router.include_router(materials_router)
router.include_router(help_request_router)
router.include_router(help_request_file_router)
router.include_router(company_router)
router.include_router(help_category_router)
router.include_router(language_router)
