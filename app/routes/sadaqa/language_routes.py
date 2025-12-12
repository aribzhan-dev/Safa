from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.sadaqa_schemas import LanguageCreate, LanguageOut
from app.services.sadaqa_service import create_language, get_languages
from app.core.db import get_session

router = APIRouter(prefix="/languages")

@router.post("/", response_model=LanguageOut)
async def add_language(data: LanguageCreate, db: AsyncSession = Depends(get_session)):
    return await create_language(db, data)

@router.get("/", response_model=list[LanguageOut])
async def list_languages(db: AsyncSession = Depends(get_session)):
    return await get_languages(db)