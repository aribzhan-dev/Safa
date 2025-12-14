import os
import uuid
from fastapi import UploadFile, HTTPException

BASE_MEDIA_PATH = "media"

IMAGE_EXT = {"jpg", "jpeg", "png", "gif", "bmp", "webp"}
VIDEO_EXT = {"mp4", "mov", "avi", "mkv", "webm"}
AUDIO_EXT = {"mp3", "ogg", "wav"}
FILE_EXT = {"pdf", "doc", "docx", "xls", "xlsx", "zip"}

def _get_folder(ext: str) -> str:
    if ext in IMAGE_EXT:
        return "img"
    if ext in VIDEO_EXT:
        return "video"
    if ext in AUDIO_EXT:
        return "audio"
    if ext in FILE_EXT:
        return "file"
    raise HTTPException(400, "Unsupported file type")


async def upload_file(file: UploadFile) -> str:
    if not file.filename:
        raise HTTPException(400, "File is required")

    ext = file.filename.split(".")[-1].lower()
    folder = _get_folder(ext)

    filename = f"{uuid.uuid4().hex}.{ext}"
    dir_path = os.path.join(BASE_MEDIA_PATH, folder)
    os.makedirs(dir_path, exist_ok=True)

    file_path = os.path.join(dir_path, filename)

    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception:
        raise HTTPException(500, "Failed to save file")

    return f"/media/{folder}/{filename}"