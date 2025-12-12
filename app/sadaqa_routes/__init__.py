from fastapi import APIRouter
from app.sadaqa_routes.company_routes import router as company_router
from app.sadaqa_routes.language_routes import router as language_router
from app.sadaqa_routes.post_routes import router as post_router
from app.sadaqa_routes.note_routes import router as note_router
from app.sadaqa_routes.materials_routes import router as materials_router
from app.sadaqa_routes.help_category_routes import router as help_category_router
from app.sadaqa_routes.help_request_routes import router as help_request_router
from app.sadaqa_routes.help_request_file_routes import router as help_request_file_router

sadaqa_router = APIRouter()

sadaqa_router.include_router(company_router, tags=["Company"])
sadaqa_router.include_router(language_router, tags=["Language"])
sadaqa_router.include_router(post_router, tags=["Post"])
sadaqa_router.include_router(note_router, tags=["Note"])
sadaqa_router.include_router(materials_router, tags=["Materials"])
sadaqa_router.include_router(help_category_router, tags=["HelpCategory"])
sadaqa_router.include_router(help_request_router, tags=["HelpRequest"])
sadaqa_router.include_router(help_request_file_router, tags=["HelpRequestFile"])