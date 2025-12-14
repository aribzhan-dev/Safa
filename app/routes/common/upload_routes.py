from fastapi import APIRouter, UploadFile, File
from app.utils.file import upload_file

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

@router.post("/")
async def upload(file: UploadFile = File(...)):
    path = await upload_file(file)
    return {
        "path": path
    }