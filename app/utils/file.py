
import uuid
import os
from fastapi import UploadFile, HTTPException

IMAGE_EXT = {"jpg", "jpeg", "png", "gif", "bmp", "webp"}
VIDEO_EXT = {"mp4", "mov", "avi", "mkv", "webm"}
AUDIO_EXT = {"mp3", "ogg"}
FILE_EXT  = {"pdf", "doc", "docx", "xls", "xlsx", "zip"}

MEDIA_ROOT = "media"


def get_extension(filename: str) -> str:
    return filename.split(".")[-1].lower()


def resolve_folder(ext: str) -> str:
    if ext in IMAGE_EXT:
        return "img"
    if ext in VIDEO_EXT:
        return "video"
    if ext in AUDIO_EXT:
        return "audio"
    if ext in FILE_EXT:
        return "file"
    raise HTTPException(400, "Unsupported file type")


def generate_filename(ext: str) -> str:
    return f"{uuid.uuid4().hex}.{ext}"


async def save_upload_file(file: UploadFile) -> str:
    ext = get_extension(file.filename)
    folder = resolve_folder(ext)
    filename = generate_filename(ext)

    os.makedirs(f"{MEDIA_ROOT}/{folder}", exist_ok=True)
    path = f"{MEDIA_ROOT}/{folder}/{filename}"

    with open(path, "wb") as f:
        content = await file.read()
        f.write(content)

    return f"/{path}"