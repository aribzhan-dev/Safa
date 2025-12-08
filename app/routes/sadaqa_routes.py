from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.sadaqa_deps import get_current_sadaqa_company
from app.core.db import get_session as get_db
from app.schemas.sadaqa_schemas import (
    LanguageCreate, LanguageOut,
    CompanyCreate, CompanyUpdate, CompanyOut,
    PostCreate, PostUpdate, PostOut,
    NoteCreate, NoteUpdate, NoteOut,
    MaterialsStatusCreate, MaterialsStatusUpdate, MaterialsStatusOut,
    HelpCategoryCreate, HelpCategoryUpdate, HelpCategoryOut,
    HelpRequestCreate, HelpRequestUpdate, HelpRequestOut,
    HelpRequestFileCreate, HelpRequestFileOut
)

from app.services.sadaqa_service import (
    create_language, get_languages,
    create_company, login_company,
    update_company,
    create_post, get_posts, update_post,
    create_note, get_notes, update_note,
    create_material_status, get_material_statuses, update_material_status,
    create_help_category, get_help_categories, update_help_category,
    create_help_request, get_help_requests, update_help_request,
    create_help_request_file
)

router = APIRouter(prefix="/sadaqa", tags=["Sadaqa"])


@router.post("/company/create", response_model=CompanyOut)
async def register_company(data: CompanyCreate, db: AsyncSession = Depends(get_db)):
    return await create_company(db, data)


@router.post("/company/login")
async def login(data: CompanyCreate, db: AsyncSession = Depends(get_db)):
    return await login_company(db, data.login, data.password)



@router.post("/languages", response_model=LanguageOut)
async def add_language(data: LanguageCreate, db: AsyncSession = Depends(get_db)):
    return await create_language(db, data)


@router.get("/languages", response_model=list[LanguageOut])
async def list_languages(db: AsyncSession = Depends(get_db)):
    return await get_languages(db)



@router.put("/company/me", response_model=CompanyOut)
async def update_my_company(
    data: CompanyUpdate,
    db: AsyncSession = Depends(get_db),
    company = Depends(get_current_sadaqa_company)
):
    return await update_company(db, company.id, data)



@router.post("/company/posts", response_model=PostOut)
async def create_my_post(
    data: PostCreate,
    db: AsyncSession = Depends(get_db),
    company = Depends(get_current_sadaqa_company)
):
    return await create_post(db, data, company)



@router.get("/company/posts", response_model=list[PostOut])
async def get_my_posts(
    db: AsyncSession = Depends(get_db),
    company = Depends(get_current_sadaqa_company)
):
    return await get_posts(db, company)


@router.put("/company/posts/{post_id}", response_model=PostOut)
async def update_my_post(
    post_id: int,
    data: PostUpdate,
    db: AsyncSession = Depends(get_db),
    company = Depends(get_current_sadaqa_company)
):
    return await update_post(db, post_id, data, company)



@router.post("/company/notes", response_model=NoteOut)
async def create_my_note(
    data: NoteCreate,
    db: AsyncSession = Depends(get_db),
    company = Depends(get_current_sadaqa_company)
):
    return await create_note(db, data, company)


@router.get("/company/notes", response_model=list[NoteOut])
async def get_my_notes(
    db: AsyncSession = Depends(get_db),
    company = Depends(get_current_sadaqa_company)
):
    return await get_notes(db, company)


@router.put("/company/notes/{note_id}", response_model=NoteOut)
async def update_my_note(
    note_id: int,
    data: NoteUpdate,
    db: AsyncSession = Depends(get_db),
    company = Depends(get_current_sadaqa_company)
):
    return await update_note(db, note_id, data, company)



@router.post("/company/materials", response_model=MaterialsStatusOut)
async def create_my_material_status(
    data: MaterialsStatusCreate,
    db: AsyncSession = Depends(get_db),
    company = Depends(get_current_sadaqa_company)
):
    return await create_material_status(db, data, company)


@router.get("/company/materials", response_model=list[MaterialsStatusOut])
async def get_my_materials_statuses(
    db: AsyncSession = Depends(get_db),
    company = Depends(get_current_sadaqa_company)
):
    return await get_material_statuses(db, company)


@router.put("/company/materials/{ms_id}", response_model=MaterialsStatusOut)
async def update_my_material_status(
    ms_id: int,
    data: MaterialsStatusUpdate,
    db: AsyncSession = Depends(get_db),
    company = Depends(get_current_sadaqa_company)
):
    return await update_material_status(db, ms_id, data, company)



@router.post("/company/categories", response_model=HelpCategoryOut)
async def create_my_help_category(
    data: HelpCategoryCreate,
    db: AsyncSession = Depends(get_db),
    company = Depends(get_current_sadaqa_company)
):
    return await create_help_category(db, data, company)


@router.get("/company/categories", response_model=list[HelpCategoryOut])
async def get_my_help_categories(
    db: AsyncSession = Depends(get_db),
    company = Depends(get_current_sadaqa_company)
):
    return await get_help_categories(db, company)


@router.put("/company/categories/{cat_id}", response_model=HelpCategoryOut)
async def update_my_help_category(
    cat_id: int,
    data: HelpCategoryUpdate,
    db: AsyncSession = Depends(get_db),
    company = Depends(get_current_sadaqa_company)
):
    return await update_help_category(db, cat_id, data, company)




@router.post("/company/help-requests", response_model=HelpRequestOut)
async def create_my_help_request(
    data: HelpRequestCreate,
    db: AsyncSession = Depends(get_db),
    company = Depends(get_current_sadaqa_company)
):
    return await create_help_request(db, data, company)


@router.get("/company/help-requests", response_model=list[HelpRequestOut])
async def get_my_help_requests(
    db: AsyncSession = Depends(get_db),
    company = Depends(get_current_sadaqa_company)
):
    return await get_help_requests(db, company)


@router.put("/company/help-requests/{hr_id}", response_model=HelpRequestOut)
async def update_my_help_request(
    hr_id: int,
    data: HelpRequestUpdate,
    db: AsyncSession = Depends(get_db),
    company = Depends(get_current_sadaqa_company)
):
    return await update_help_request(db, hr_id, data, company)



@router.post("/company/help-requests/files", response_model=HelpRequestFileOut)
async def upload_my_help_request_file(
    data: HelpRequestFileCreate,
    db: AsyncSession = Depends(get_db),
    company = Depends(get_current_sadaqa_company)
):
    return await create_help_request_file(db, data, company)