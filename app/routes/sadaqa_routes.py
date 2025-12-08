from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas.sadaqa_schemas import (
    LanguageCreate,
    CompanyCreate, CompanyUpdate,
    PostCreate, PostUpdate,
    NoteCreate, NoteUpdate,
    MaterialsStatusCreate, MaterialsStatusUpdate,
    HelpCategoryCreate, HelpCategoryUpdate,
    HelpRequestCreate, HelpRequestUpdate,
    HelpRequestFileCreate
)

from app.services.sadaqa_service import (
    create_language, get_language, get_languages, update_language,
    create_company, get_company, get_companies, update_company,
    create_post, get_post, get_posts, update_post,
    create_note, get_note, get_notes, update_note,
    create_material_status, get_material_status, get_material_statuses, update_material_status,
    create_help_category, get_help_category, update_help_category,
    create_help_request, get_help_request, get_help_requests, update_help_request,
    create_help_request_file
)


router = APIRouter(prefix="/sadaqa", tags=["Sadaqa System"])



@router.post("/languages")
async def create_lang(data: LanguageCreate, db: AsyncSession = Depends(get_session)):
    return await create_language(db, data)


@router.get("/languages")
async def list_languages(db: AsyncSession = Depends(get_session)):
    return await get_languages(db)


@router.get("/languages/{lang_id}")
async def get_lang(lang_id: int, db: AsyncSession = Depends(get_session)):
    return await get_language(db, lang_id)




@router.post("/companies")
async def create_comp(data: CompanyCreate, db: AsyncSession = Depends(get_session)):
    return await create_company(db, data)


@router.get("/companies")
async def list_companies(db: AsyncSession = Depends(get_session)):
    return await get_companies(db)


@router.get("/companies/{company_id}")
async def get_comp(company_id: int, db: AsyncSession = Depends(get_session)):
    return await get_company(db, company_id)


@router.patch("/companies/{company_id}")
async def patch_company(
    company_id: int,
    data: CompanyUpdate,
    db: AsyncSession = Depends(get_session)
):
    return await update_company(db, company_id, data)
