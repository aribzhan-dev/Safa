import os
import uuid
from fastapi import UploadFile, HTTPException

BASE_MEDIA_PATH = "media"

IMAGE_EXT = {"jpg", "jpeg", "png", "gif", "bmp", "webp"}
VIDEO_EXT = {"mp4", "mov", "avi", "mkv", "webm"}
AUDIO_EXT = {"mp3", "ogg", "wav"}
FILE_EXT = {"pdf", "doc", "docx", "xls", "xlsx", "zip"}


def _detect_folder(ext: str) -> str:
    if ext in IMAGE_EXT:
        return "img"
    if ext in VIDEO_EXT:
        return "video"
    if ext in AUDIO_EXT:
        return "audio"
    if ext in FILE_EXT:
        return "file"
    raise HTTPException(status_code=400, detail="Unsupported file type")


async def upload_file(file: UploadFile) -> str:
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="File is required")

    ext = file.filename.split(".")[-1].lower()
    folder = _detect_folder(ext)

    filename = f"{uuid.uuid4().hex}.{ext}"
    dir_path = os.path.join(BASE_MEDIA_PATH, folder)
    os.makedirs(dir_path, exist_ok=True)

    full_path = os.path.join(dir_path, filename)

    try:
        contents = await file.read()
        with open(full_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail="File save failed")

    return f"/media/{folder}/{filename}"