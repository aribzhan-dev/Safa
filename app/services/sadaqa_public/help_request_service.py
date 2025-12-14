from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.sadaqa import HelpRequest
from app.schemas.sadaqa_schemas import HelpRequestCreate

async def create_help_request(
    db: AsyncSession,
    data: HelpRequestCreate
):
    hr = HelpRequest(**data.model_dump())
    db.add(hr)
    await db.commit()
    await db.refresh(hr)
    return hr


