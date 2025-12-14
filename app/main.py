from fastapi import FastAPI
import uvicorn

from app.routes.sadaqa.private_routes import router as private_sadaqa_router
from app.routes.sadaqa.public_routes import router as public_sadaqa_router
from app.routes.common.upload_routes import router as upload_file
app = FastAPI(title="Safa API")
app.security = [{"HTTPBearer": []}]

app.include_router(private_sadaqa_router, prefix="/api/sadaqa/private")
app.include_router(public_sadaqa_router, prefix="/api/sadaqa/public")
app.include_router(upload_file, prefix="/api/upload")

# @app.get("/api/")
# async def root():
#     return {"message": "FastAPI is working!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1")
