from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, UploadFile
from app.models.sadaqa import HelpRequest, HelpRequestFile, Company


async def create_help_request_file(
    db: AsyncSession,
    help_request_id: int,
    file_path: str
):
    r = await db.execute(
        select(HelpRequest).where(HelpRequest.id == help_request_id)
    )
    hr = r.scalar_one_or_none()

    if not hr:
        raise HTTPException(404, "Help request not found")


    file = HelpRequestFile(
        help_request_id=help_request_id,
        filename=file_path
    )
    db.add(file)
    await db.commit()
    await db.refresh(file)
    return file





