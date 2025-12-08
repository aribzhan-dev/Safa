from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.sadaqa import (
    Company, CompanyAuth,
    Language, Post, Note,
    MaterialsStatus, HelpCategory,
    HelpRequest, HelpRequestFile
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

from app.core.security import hash_password, verify_password
from app.core.jwt import create_tokens


async def create_company(db: AsyncSession, data: CompanyCreate):
    company = Company(
        title=data.title,
        why_collecting=data.why_collecting,
        image=data.image
    )

    db.add(company)
    await db.flush()


    auth = CompanyAuth(
        company_id=company.id,
        login=data.login,
        password_hash=hash_password(data.password)
    )

    db.add(auth)
    await db.commit()
    await db.refresh(company)
    return company


async def login_company(db: AsyncSession, login: str, password: str):
    result = await db.execute(
        select(CompanyAuth).where(CompanyAuth.login == login)
    )
    auth = result.scalar_one_or_none()

    if not auth:
        raise HTTPException(401, "Invalid login or password")

    if not verify_password(password, auth.password_hash):
        raise HTTPException(401, "Invalid login or password")

    access, refresh = create_tokens({"company_id": auth.company_id})

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }


async def update_company(db: AsyncSession, company_id: int, data: CompanyUpdate):
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(404, "Company not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(company, key, value)

    await db.commit()
    await db.refresh(company)
    return company




async def create_language(db: AsyncSession, data: LanguageCreate):
    lang = Language(**data.model_dump())
    db.add(lang)
    await db.commit()
    await db.refresh(lang)
    return lang


async def get_languages(db: AsyncSession):
    r = await db.execute(select(Language))
    return r.scalars().all()



async def create_post(db: AsyncSession, data: PostCreate, company: Company):
    post = Post(
        company_id=company.id,
        language_id=data.language_id,
        image=data.image,
        title=data.title,
        content=data.content
    )

    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def get_posts(db: AsyncSession, company: Company):
    r = await db.execute(
        select(Post).where(Post.company_id == company.id)
    )
    return r.scalars().all()


async def update_post(db: AsyncSession, post_id: int, data: PostUpdate, company: Company):
    r = await db.execute(
        select(Post).where(Post.id == post_id, Post.company_id == company.id)
    )
    post = r.scalar_one_or_none()

    if not post:
        raise HTTPException(404, "Post not found or no permission")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(post, key, value)

    await db.commit()
    await db.refresh(post)
    return post




async def create_note(db: AsyncSession, data: NoteCreate, company: Company):
    if data.collected_money > data.goal_money:
        raise HTTPException(400, "collected_money cannot exceed goal_money")

    note = Note(
        company_id=company.id,
        **data.model_dump()
    )

    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def get_notes(db: AsyncSession, company: Company):
    r = await db.execute(
        select(Note).where(Note.company_id == company.id)
    )
    return r.scalars().all()


async def update_note(db: AsyncSession, note_id: int, data: NoteUpdate, company: Company):
    r = await db.execute(
        select(Note).where(Note.id == note_id, Note.company_id == company.id)
    )
    note = r.scalar_one_or_none()

    if not note:
        raise HTTPException(404, "Note not found or no permission")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(note, key, value)

    if note.collected_money > note.goal_money:
        raise HTTPException(400, "collected_money cannot exceed goal_money")

    await db.commit()
    await db.refresh(note)
    return note




async def create_material_status(db: AsyncSession, data: MaterialsStatusCreate, company: Company):
    ms = MaterialsStatus(
        company_id=company.id,
        language_id=data.language_id,
        title=data.title,
        status=1
    )

    db.add(ms)
    await db.commit()
    await db.refresh(ms)
    return ms


async def get_material_statuses(db: AsyncSession, company: Company):
    r = await db.execute(
        select(MaterialsStatus).where(MaterialsStatus.company_id == company.id)
    )
    return r.scalars().all()


async def update_material_status(db: AsyncSession, ms_id: int, data: MaterialsStatusUpdate, company: Company):
    r = await db.execute(
        select(MaterialsStatus).where(
            MaterialsStatus.id == ms_id,
            MaterialsStatus.company_id == company.id
        )
    )
    ms = r.scalar_one_or_none()

    if not ms:
        raise HTTPException(404, "MaterialsStatus not found or no permission")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(ms, key, value)

    await db.commit()
    await db.refresh(ms)
    return ms




async def create_help_category(db: AsyncSession, data: HelpCategoryCreate, company: Company):
    cat = HelpCategory(
        company_id=company.id,
        language_id=data.language_id,
        title=data.title,
        is_other=data.is_other,
        status=1
    )

    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return cat


async def get_help_categories(db: AsyncSession, company: Company):
    r = await db.execute(
        select(HelpCategory).where(HelpCategory.company_id == company.id)
    )
    return r.scalars().all()


async def update_help_category(db: AsyncSession, cat_id: int, data: HelpCategoryUpdate, company: Company):
    r = await db.execute(
        select(HelpCategory).where(
            HelpCategory.id == cat_id,
            HelpCategory.company_id == company.id
        )
    )
    cat = r.scalar_one_or_none()

    if not cat:
        raise HTTPException(404, "Category not found or no permission")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(cat, key, value)

    await db.commit()
    await db.refresh(cat)
    return cat




async def create_help_request(db: AsyncSession, data: HelpRequestCreate, company: Company):
    hr = HelpRequest(
        company_id=company.id,
        **data.model_dump()
    )

    db.add(hr)
    await db.commit()
    await db.refresh(hr)
    return hr


async def get_help_requests(db: AsyncSession, company: Company):
    r = await db.execute(
        select(HelpRequest).where(HelpRequest.company_id == company.id)
    )
    return r.scalars().all()


async def update_help_request(db: AsyncSession, hr_id: int, data: HelpRequestUpdate, company: Company):
    r = await db.execute(
        select(HelpRequest).where(
            HelpRequest.id == hr_id,
            HelpRequest.company_id == company.id
        )
    )
    hr = r.scalar_one_or_none()

    if not hr:
        raise HTTPException(404, "HelpRequest not found or no permission")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(hr, key, value)

    await db.commit()
    await db.refresh(hr)
    return hr



async def create_help_request_file(db: AsyncSession, data: HelpRequestFileCreate, company: Company):

    result = await db.execute(
        select(HelpRequest).where(
            HelpRequest.id == data.help_request_id,
            HelpRequest.company_id == company.id
        )
    )
    hr = result.scalar_one_or_none()

    if not hr:
        raise HTTPException(404, "HelpRequest not found or no permission")

    file = HelpRequestFile(
        help_request_id=data.help_request_id,
        filename=data.filename
    )

    db.add(file)
    await db.commit()
    await db.refresh(file)
    return file