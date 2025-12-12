from fastapi import FastAPI
import uvicorn
from app.routes.tour_routes import router as tour_routes
from app.sadaqa_routes import sadaqa_router


app = FastAPI(title="Safa API")

app.include_router(sadaqa_router, prefix="/api/sadaqa")

app.include_router(tour_routes, prefix="/api/tour")

@app.get("/api/")
async def root():
    return {"message": "FastAPI is working!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1")
