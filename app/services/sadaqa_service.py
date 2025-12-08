from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.sadaqa import (
    Language, Company, CompanyAuth, Post, Note,
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
from app.core.security import hash_password, verify_password
from app.core.jwt import create_tokens



async def create_language(db: AsyncSession, data: LanguageCreate):
    lang = Language(**data.model_dump())
    db.add(lang)
    await db.commit()
    await db.refresh(lang)
    return lang


async def get_languages(db: AsyncSession):
    result = await db.execute(select(Language))
    return result.scalars().all()




async def create_company(db: AsyncSession, data: CompanyCreate):
    company = Company(**data.model_dump())
    db.add(company)
    await db.commit()
    await db.refresh(company)
    return company


async def login_company(db: AsyncSession, login: str, password: str):
    result = await db.execute(select(CompanyAuth).where(CompanyAuth.login == login))
    auth = result.scalar_one_or_none()

    if not auth:
        raise HTTPException(401, "Invalid login or password")

    if not verify_password(password, auth.password_hash):
        raise HTTPException(401, "Invalid login or password")

    access, refresh = create_tokens({"company_id": auth.company_id})

    return {"access_token": access, "refresh_token": refresh, "type": "bearer"}


async def update_company(db: AsyncSession, company_id: int, data: CompanyUpdate):
    comp = await db.get(Company, company_id)
    if not comp:
        raise HTTPException(404, "Company not found")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(comp, k, v)

    await db.commit()
    await db.refresh(comp)
    return comp




async def create_post(db: AsyncSession, data: PostCreate, company):
    post = Post(company_id=company.id, **data.model_dump())
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def get_posts(db: AsyncSession, company):
    result = await db.execute(
        select(Post).where(Post.company_id == company.id)
    )
    return result.scalars().all()


async def update_post(db: AsyncSession, post_id: int, data: PostUpdate, company):
    post = await db.get(Post, post_id)
    if not post or post.company_id != company.id:
        raise HTTPException(404, "Post not found or no access")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(post, k, v)

    await db.commit()
    await db.refresh(post)
    return post



async def create_note(db: AsyncSession, data: NoteCreate, company):
    if data.collected_money > data.goal_money:
        raise HTTPException(400, "Collected > goal")

    note = Note(company_id=company.id, **data.model_dump())
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def get_notes(db: AsyncSession, company):
    result = await db.execute(select(Note).where(Note.company_id == company.id))
    return result.scalars().all()


async def update_note(db: AsyncSession, note_id: int, data: NoteUpdate, company):
    note = await db.get(Note, note_id)
    if not note or note.company_id != company.id:
        raise HTTPException(404, "Note not found or no permission")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(note, k, v)

    if note.collected_money > note.goal_money:
        raise HTTPException(400, "Collected > Goal")

    await db.commit()
    await db.refresh(note)
    return note




async def create_material_status(db: AsyncSession, data: MaterialsStatusCreate, company):
    ms = MaterialsStatus(company_id=company.id, **data.model_dump())
    db.add(ms)
    await db.commit()
    await db.refresh(ms)
    return ms


async def get_material_statuses(db: AsyncSession, company):
    result = await db.execute(
        select(MaterialsStatus).where(MaterialsStatus.company_id == company.id)
    )
    return result.scalars().all()


async def update_material_status(db: AsyncSession, ms_id: int, data: MaterialsStatusUpdate, company):
    ms = await db.get(MaterialsStatus, ms_id)
    if not ms or ms.company_id != company.id:
        raise HTTPException(404, "Material status not found or no permission")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(ms, k, v)

    await db.commit()
    await db.refresh(ms)
    return ms




async def create_help_category(db: AsyncSession, data: HelpCategoryCreate, company):
    cat = HelpCategory(company_id=company.id, **data.model_dump())
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return cat


async def get_help_categories(db: AsyncSession, company):
    result = await db.execute(
        select(HelpCategory).where(HelpCategory.company_id == company.id)
    )
    return result.scalars().all()


async def update_help_category(db: AsyncSession, cat_id: int, data: HelpCategoryUpdate, company):
    cat = await db.get(HelpCategory, cat_id)
    if not cat or cat.company_id != company.id:
        raise HTTPException(404, "Category not found or no permission")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(cat, k, v)

    await db.commit()
    await db.refresh(cat)
    return cat




async def create_help_request(db: AsyncSession, data: HelpRequestCreate, company):
    hr = HelpRequest(company_id=company.id, **data.model_dump())
    db.add(hr)
    await db.commit()
    await db.refresh(hr)
    return hr


async def get_help_requests(db: AsyncSession, company):
    result = await db.execute(
        select(HelpRequest).where(HelpRequest.company_id == company.id)
    )
    return result.scalars().all()


async def update_help_request(db: AsyncSession, hr_id: int, data: HelpRequestUpdate, company):
    hr = await db.get(HelpRequest, hr_id)
    if not hr or hr.company_id != company.id:
        raise HTTPException(404, "Help Request not found or access forbidden")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(hr, k, v)

    await db.commit()
    await db.refresh(hr)
    return hr



async def create_help_request_file(db: AsyncSession, data: HelpRequestFileCreate, company):
    hr = await db.get(HelpRequest, data.help_request_id)
    if not hr or hr.company_id != company.id:
        raise HTTPException(404, "Help Request not found or no permission")

    file = HelpRequestFile(**data.model_dump())
    db.add(file)
    await db.commit()
    await db.refresh(file)
    return file