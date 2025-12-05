from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.sadaqa import (
    Language, Company, Post, Note,
    MaterialsStatus, HelpCategory, HelpRequest, HelpRequestFile
)
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





async def create_language(db: AsyncSession, data: LanguageCreate):
    lang = Language(**data.model_dump())
    db.add(lang)
    await db.commit()
    await db.refresh(lang)
    return lang


async def get_language(db: AsyncSession, lang_id: int):
    result = await db.execute(select(Language).where(Language.id == lang_id))
    lang = result.scalar_one_or_none()

    if not lang:
        raise HTTPException(404, "Language not found")

    return lang


async def get_languages(db: AsyncSession):
    result = await db.execute(select(Language))
    return result.scalars().all()


async def update_language(db: AsyncSession, lang_id: int, data: LanguageUpdate):
    lang = await get_language(db, lang_id)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(lang, key, value)

    await db.commit()
    await db.refresh(lang)
    return lang






async def create_company(db: AsyncSession, data: CompanyCreate):
    comp = Company(**data.model_dump())
    db.add(comp)
    await db.commit()
    await db.refresh(comp)
    return comp


async def get_company(db: AsyncSession, company_id: int):
    result = await db.execute(select(Company).where(Company.id == company_id))
    comp = result.scalar_one_or_none()
    if not comp:
        raise HTTPException(404, "Company not found")
    return comp


async def get_companies(db: AsyncSession):
    result = await db.execute(select(Company))
    return result.scalars().all()


async def update_company(db: AsyncSession, company_id: int, data: CompanyUpdate):
    comp = await get_company(db, company_id)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(comp, key, value)

    await db.commit()
    await db.refresh(comp)
    return comp






async def create_post(db: AsyncSession, data: PostCreate):
    # check language exists
    await get_language(db, data.language_id)

    post = Post(**data.model_dump())
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def get_post(db: AsyncSession, post_id: int):
    r = await db.execute(select(Post).where(Post.id == post_id))
    post = r.scalar_one_or_none()
    if not post:
        raise HTTPException(404, "Post not found")
    return post


async def get_posts(db: AsyncSession, lang_id: int | None = None):
    query = select(Post)
    if lang_id:
        query = query.where(Post.language_id == lang_id)

    r = await db.execute(query)
    return r.scalars().all()


async def update_post(db: AsyncSession, post_id: int, data: PostUpdate):
    post = await get_post(db, post_id)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(post, key, value)

    await db.commit()
    await db.refresh(post)
    return post






async def create_note(db: AsyncSession, data: NoteCreate):
    await get_language(db, data.language_id)

    note = Note(**data.model_dump())

    # Extra business rule
    if note.collected_money > note.goal_money:
        raise HTTPException(400, "collected_money cannot exceed goal_money")

    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def get_note(db: AsyncSession, note_id: int):
    r = await db.execute(select(Note).where(Note.id == note_id))
    note = r.scalar_one_or_none()
    if not note:
        raise HTTPException(404, "Note not found")
    return note


async def get_notes(db: AsyncSession):
    r = await db.execute(select(Note))
    return r.scalars().all()


async def update_note(db: AsyncSession, note_id: int, data: NoteUpdate):
    note = await get_note(db, note_id)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(note, key, value)

    if note.collected_money and note.goal_money:
        if note.collected_money > note.goal_money:
            raise HTTPException(400, "collected_money cannot exceed goal_money")

    await db.commit()
    await db.refresh(note)
    return note





async def create_material_status(db: AsyncSession, data: MaterialsStatusCreate):
    # validate language
    await get_language(db, data.language_id)

    ms = MaterialsStatus(**data.model_dump())
    db.add(ms)
    await db.commit()
    await db.refresh(ms)
    return ms


async def get_material_status(db: AsyncSession, ms_id: int):
    r = await db.execute(select(MaterialsStatus).where(MaterialsStatus.id == ms_id))
    ms = r.scalar_one_or_none()
    if not ms:
        raise HTTPException(404, "MaterialsStatus not found")
    return ms


async def get_material_statuses(db: AsyncSession):
    r = await db.execute(select(MaterialsStatus))
    return r.scalars().all()


async def update_material_status(db: AsyncSession, ms_id: int, data: MaterialsStatusUpdate):
    ms = await get_material_status(db, ms_id)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(ms, key, value)

    await db.commit()
    await db.refresh(ms)
    return ms





async def create_help_category(db: AsyncSession, data: HelpCategoryCreate):
    await get_language(db, data.language_id)

    hc = HelpCategory(**data.model_dump())
    db.add(hc)
    await db.commit()
    await db.refresh(hc)
    return hc


async def get_help_category(db: AsyncSession, cat_id: int):
    r = await db.execute(select(HelpCategory).where(HelpCategory.id == cat_id))
    hc = r.scalar_one_or_none()
    if not hc:
        raise HTTPException(404, "Help Category not found")
    return hc


async def update_help_category(db: AsyncSession, cat_id: int, data: HelpCategoryUpdate):
    hc = await get_help_category(db, cat_id)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(hc, key, value)

    await db.commit()
    await db.refresh(hc)
    return hc




async def create_help_request(db: AsyncSession, data: HelpRequestCreate):


    await get_material_status(db, data.materials_status_id)
    await get_help_category(db, data.help_category_id)

    hr = HelpRequest(**data.model_dump())
    db.add(hr)
    await db.commit()
    await db.refresh(hr)
    return hr


async def get_help_request(db: AsyncSession, hr_id: int):
    r = await db.execute(select(HelpRequest).where(HelpRequest.id == hr_id))
    hr = r.scalar_one_or_none()
    if not hr:
        raise HTTPException(404, "Help Request not found")
    return hr


async def get_help_requests(db: AsyncSession):
    r = await db.execute(select(HelpRequest))
    return r.scalars().all()


async def update_help_request(db: AsyncSession, hr_id: int, data: HelpRequestUpdate):
    hr = await get_help_request(db, hr_id)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(hr, key, value)

    await db.commit()
    await db.refresh(hr)
    return hr



async def create_help_request_file(db: AsyncSession, data: HelpRequestFileCreate):
    await get_help_request(db, data.help_request_id)

    f = HelpRequestFile(**data.model_dump())
    db.add(f)
    await db.commit()
    await db.refresh(f)
    return f