from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.sadaqa import (
    Language, Company, CompanyAuth,
    Post, Note, MaterialsStatus,
    HelpCategory, HelpRequest, HelpRequestFile
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

    exists = await db.execute(
        select(CompanyAuth).where(CompanyAuth.login == data.login)
    )
    if exists.scalar_one_or_none():
        raise HTTPException(400, "Login already exists")

    company = Company(
        title=data.title,
        image=data.image,
        why_collecting=data.why_collecting,
    )
    db.add(company)
    await db.commit()
    await db.refresh(company)

    auth = CompanyAuth(
        company_id=company.id,
        login=data.login,
        password_hash=hash_password(data.password)
    )
    db.add(auth)
    await db.commit()
    return company



async def login_company(db: AsyncSession, login: str, password: str):

    result = await db.execute(
        select(CompanyAuth).where(CompanyAuth.login == login)
    )
    auth = result.scalar_one_or_none()

    if not auth or not verify_password(password, auth.password_hash):
        raise HTTPException(401, "Invalid login or password")

    access, refresh = create_tokens({"company_id": auth.company_id})

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }



async def create_language(db: AsyncSession, data: LanguageCreate):
    lang = Language(**data.model_dump())
    db.add(lang)
    await db.commit()
    await db.refresh(lang)
    return lang


async def get_language(db: AsyncSession, lang_id: int):
    r = await db.execute(select(Language).where(Language.id == lang_id))
    lang = r.scalar_one_or_none()
    if not lang:
        raise HTTPException(404, "Language not found")
    return lang




async def create_post(db: AsyncSession, data: PostCreate, current_company: Company):

    await get_language(db, data.language_id)

    post = Post(
        company_id=current_company.id,
        language_id=data.language_id,
        image=data.image,
        title=data.title,
        content=data.content,
    )

    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def get_posts(db: AsyncSession, current_company: Company, lang_id: int | None = None):

    query = select(Post).where(Post.company_id == current_company.id)

    if lang_id:
        query = query.where(Post.language_id == lang_id)

    r = await db.execute(query)
    return r.scalars().all()


async def update_post(db: AsyncSession, post_id: int, data: PostUpdate, current_company: Company):

    r = await db.execute(
        select(Post).where(Post.id == post_id, Post.company_id == current_company.id)
    )
    post = r.scalar_one_or_none()
    if not post:
        raise HTTPException(404, "Post not found or no permission")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(post, key, value)

    await db.commit()
    await db.refresh(post)
    return post




async def create_note(db: AsyncSession, data: NoteCreate, current_company: Company):

    await get_language(db, data.language_id)

    if data.collected_money > data.goal_money:
        raise HTTPException(400, "collected_money cannot exceed goal_money")

    note = Note(
        company_id=current_company.id,
        **data.model_dump()
    )

    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def get_notes(db: AsyncSession, current_company: Company):

    r = await db.execute(
        select(Note).where(Note.company_id == current_company.id)
    )
    return r.scalars().all()


async def update_note(db: AsyncSession, note_id: int, data: NoteUpdate, current_company: Company):

    r = await db.execute(
        select(Note).where(Note.id == note_id, Note.company_id == current_company.id)
    )
    note = r.scalar_one_or_none()

    if not note:
        raise HTTPException(404, "Note not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(note, key, value)

    if note.collected_money > note.goal_money:
        raise HTTPException(400, "Invalid: collected > goal")

    await db.commit()
    await db.refresh(note)
    return note




async def create_material_status(db: AsyncSession, data: MaterialsStatusCreate, current_company: Company):

    await get_language(db, data.language_id)

    ms = MaterialsStatus(
        company_id=current_company.id,
        **data.model_dump()
    )
    db.add(ms)
    await db.commit()
    await db.refresh(ms)
    return ms


async def get_material_statuses(db: AsyncSession, current_company: Company):
    r = await db.execute(
        select(MaterialsStatus).where(MaterialsStatus.company_id == current_company.id)
    )
    return r.scalars().all()




async def create_help_category(db: AsyncSession, data: HelpCategoryCreate, current_company: Company):
    await get_language(db, data.language_id)

    cat = HelpCategory(
        company_id=current_company.id,
        **data.model_dump()
    )
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return cat


async def get_help_categories(db: AsyncSession, current_company: Company):
    r = await db.execute(
        select(HelpCategory).where(
            HelpCategory.company_id == current_company.id
        )
    )
    return r.scalars().all()



async def create_help_request(db: AsyncSession, data: HelpRequestCreate, current_company: Company):

    ms = await db.execute(
        select(MaterialsStatus).where(
            MaterialsStatus.id == data.materials_status_id,
            MaterialsStatus.company_id == current_company.id
        )
    )
    if not ms.scalar_one_or_none():
        raise HTTPException(400, "Invalid materials_status_id")

    hc = await db.execute(
        select(HelpCategory).where(
            HelpCategory.id == data.help_category_id,
            HelpCategory.company_id == current_company.id
        )
    )
    if not hc.scalar_one_or_none():
        raise HTTPException(400, "Invalid help_category_id")

    req = HelpRequest(
        company_id=current_company.id,
        **data.model_dump()
    )

    db.add(req)
    await db.commit()
    await db.refresh(req)
    return req


async def get_help_requests(db: AsyncSession, current_company: Company):

    r = await db.execute(
        select(HelpRequest).where(
            HelpRequest.company_id == current_company.id
        )
    )
    return r.scalars().all()



async def create_help_request_file(db: AsyncSession, data: HelpRequestFileCreate, current_company: Company):

    hr = await db.execute(
        select(HelpRequest).where(
            HelpRequest.id == data.help_request_id,
            HelpRequest.company_id == current_company.id
        )
    )
    if not hr.scalar_one_or_none():
        raise HTTPException(404, "HelpRequest not found")

    file = HelpRequestFile(
        help_request_id=data.help_request_id,
        filename=data.filename
    )

    db.add(file)
    await db.commit()
    await db.refresh(file)
    return file