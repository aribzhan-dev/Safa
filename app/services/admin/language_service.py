from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sadaqa import Language
from app.schemas.sadaqa_schemas import LanguageCreate



async def create_language(db: AsyncSession, data: LanguageCreate):
    lang = Language(**data.model_dump())
    db.add(lang)
    await db.commit()
    await db.refresh(lang)
    return lang


async def get_languages(db: AsyncSession):
    r = await db.execute(select(Language))
    return r.scalars().all()