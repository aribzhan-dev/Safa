from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.routes.sadaqa.private_routes import router as private_sadaqa_router
from app.routes.sadaqa.public_routes import router as public_sadaqa_router
from app.routes.tours.private_routes import router as private_tours_router
from app.routes.tours.public_routes import router as public_tours_router
from app.routes.common.upload_routes import router as upload_router


app = FastAPI(
    title="Safa API",
    security=[{"HTTPBearer": []}],
    version="1.0.0",
    openapi_tags=[
        {"name": "Sadaqa | Company (Private)"},
        {"name": "Sadaqa | Public"},
        {"name": "Tour | Company (Private)"},
        {"name": "Tour | Public"},
        {"name": "Upload"},
    ],
)


app.include_router(
    private_sadaqa_router,
    prefix="/api/sadaqa/private",
)

app.include_router(
    public_sadaqa_router,
    prefix="/api/sadaqa/public",
)

app.include_router(
    private_tours_router,
    prefix="/api/tour/private",
)

app.include_router(
    public_tours_router,
    prefix="/api/tour/public",
)

app.include_router(
    upload_router,
    prefix="/api",
)

app.mount(
    "/media",
    StaticFiles(directory="media"),
    name="media",
)

@app.get("/")
def root():
    return {"status": "ok"}




if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, host="127.0.0.1", port=8080)