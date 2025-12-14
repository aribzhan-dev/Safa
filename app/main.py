from fastapi import FastAPI
import uvicorn
from app.routes.tour_routes import router as tour_routes
from app.sadaqa_routes import sadaqa_router
from app.routes.sadaqa.public_routes import router as public_company_router
from app.routes.sadaqa.private_routes import router as private_company_router

app = FastAPI(title="Safa API")
app.security = [{"HTTPBearer": []}]

app.include_router(
    private_company_router,
    prefix="/api/sadaqa/private"
)

app.include_router(
    public_company_router,
    prefix="/api/sadaqa/public"
)
app.include_router(tour_routes, prefix="/api/tour")

@app.get("/api/")
async def root():
    return {"message": "FastAPI is working!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1")
