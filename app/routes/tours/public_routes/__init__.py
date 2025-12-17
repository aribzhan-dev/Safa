from fastapi import APIRouter
from app.routes.tours.public_routes.tour_routes import router as tour_router
from app.routes.tours.public_routes.company_routes import router as company_router
from app.routes.tours.public_routes.booking_routes import router as booking_router
from app.routes.tours.public_routes.guide_routes import router as guide_router
from app.routes.tours.public_routes.category_routes import router as category_router


router = APIRouter()

router.include_router(company_router, tags=["Company"])
router.include_router(tour_router, tags=["Tours"])
router.include_router(booking_router, tags=["Booking"])
router.include_router(guide_router, tags=["Guide"])
router.include_router(category_router, tags=["Category"])
