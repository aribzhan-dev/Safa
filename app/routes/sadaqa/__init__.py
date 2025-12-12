from fastapi import APIRouter

from app.routes.sadaqa.company_routes import router as company_router
from app.routes.sadaqa.language_routes import router as language_router
from app.routes.sadaqa.post_routes import router as post_router
from app.routes.sadaqa.note_routes import router as note_router
from app.routes.sadaqa.materials_routes import router as materials_router
from app.routes.sadaqa.help_category_routes import router as help_category_router
from app.routes.sadaqa.help_request_routes import router as help_request_router
from app.routes.sadaqa.help_request_file_routes import router as help_request_file_router

sadaqa_router = APIRouter(prefix="/sadaqa", tags=["Sadaqa"])

sadaqa_router.include_router(company_router)
sadaqa_router.include_router(language_router)
sadaqa_router.include_router(post_router)
sadaqa_router.include_router(note_router)
sadaqa_router.include_router(materials_router)
sadaqa_router.include_router(help_category_router)
sadaqa_router.include_router(help_request_router)
sadaqa_router.include_router(help_request_file_router)