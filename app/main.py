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


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = FastAPI.openapi(app)

    openapi_schema["components"]["securitySchemes"] = {
        "sadaqaAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Sadaqa Company Access Token",
        },
        "tourAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Tour Company Access Token",
        },
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)