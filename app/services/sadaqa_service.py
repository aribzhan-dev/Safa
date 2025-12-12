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
import uuid



IMAGE_EXT = {"jpg", "jpeg", "png", "gif", "bmp", "webp"}
VIDEO_EXT = {"mp4", "mov", "avi", "mkv", "webm"}
AUDIO_EXT = {"mp3", "ogg"}
FILE_EXT = {"pdf", "doc", "docx", "xls", "xlsx", "zip"}


def generate_filename(original_name: str) -> str:
    ext = original_name.split(".")[-1].lower()
    return f"{uuid.uuid4().hex}.{ext}"


def build_file_path(original_name: str) -> str:
    ext = original_name.split(".")[-1].lower()

    if ext in IMAGE_EXT:
        folder = "/media/img/"
    elif ext in VIDEO_EXT:
        folder = "/media/video/"
    elif ext in AUDIO_EXT:
        folder = "/media/audio/"
    else:
        folder = "/media/file/"

    return folder + generate_filename(original_name)



async def create_company(db: AsyncSession, data: CompanyCreate):
    company = Company(
        title=data.title,
        why_collecting=data.why_collecting,
        image=data.image,
        payment=data.payment,
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

    if not auth or not verify_password(password, auth.password_hash):
        raise HTTPException(401, "Invalid login or password")

    access, refresh = create_tokens({
        "company_auth_id": auth.id,
        "role": "company"
    })

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "Bearer"
    }


async def update_company(db: AsyncSession, company_id: int, data: CompanyUpdate):
    result = await db.execute(
        select(Company).where(Company.id == company_id)
    )
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(404, "Company not found")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(company, k, v)

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
        **data.model_dump()
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
        select(Post).where(
            Post.id == post_id,
            Post.company_id == company.id
        )
    )
    post = r.scalar_one_or_none()

    if not post:
        raise HTTPException(404, "Post not found or no permission")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(post, k, v)

    await db.commit()
    await db.refresh(post)
    return post




async def create_note(db: AsyncSession, data: NoteCreate, company: Company):
    if data.collected_money > data.goal_money:
        raise HTTPException(400, "Collected money cannot exceed goal")

    note = Note(company_id=company.id, **data.model_dump())
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
        select(Note).where(
            Note.id == note_id,
            Note.company_id == company.id
        )
    )
    note = r.scalar_one_or_none()

    if not note:
        raise HTTPException(404, "Note not found or no permission")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(note, k, v)

    if note.collected_money > note.goal_money:
        raise HTTPException(400, "Collected money cannot exceed goal")

    await db.commit()
    await db.refresh(note)
    return note




async def create_material_status(db: AsyncSession, data: MaterialsStatusCreate, company: Company):
    ms = MaterialsStatus(
        company_id=company.id,
        **data.model_dump()
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


async def create_help_category(db: AsyncSession, data: HelpCategoryCreate, company: Company):
    cat = HelpCategory(
        company_id=company.id,
        **data.model_dump()
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




async def public_create_help_request(db: AsyncSession, data: HelpRequestCreate):
    hr = HelpRequest(**data.model_dump())
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

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(hr, k, v)

    await db.commit()
    await db.refresh(hr)
    return hr



async def create_help_request_file(
    db: AsyncSession,
    data: HelpRequestFileCreate,
    company: Company
):
    r = await db.execute(
        select(HelpRequest).where(
            HelpRequest.id == data.help_request_id,
            HelpRequest.company_id == company.id
        )
    )
    req = r.scalar_one_or_none()

    if not req:
        raise HTTPException(404, "Help request not found or no permission")

    file_path = build_file_path(data.filename)

    file = HelpRequestFile(
        help_request_id=data.help_request_id,
        filename=file_path
    )
    db.add(file)
    await db.commit()
    await db.refresh(file)
    return file