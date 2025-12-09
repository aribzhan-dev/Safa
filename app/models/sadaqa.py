from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from sqlalchemy.sql import func
from enum import Enum, IntEnum
from sqlalchemy import (
    String, Integer, DateTime,
    Enum as SqlEnum, Float,
    ForeignKey, Text, Boolean
)
from datetime import datetime
from typing import List


class TypeChoices(str, Enum):
    normal = "Обычный"
    medium = "Средний"
    urgent = "Срочный"
    very_urgent = "Очень срочный"


class StatusEnum(IntEnum):
    active = 0
    inactive = 1
    archived = 2


class CompanyAuth(Base):
    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id"),
        nullable=False,
        unique=True,
    )
    login: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    company: Mapped["Company"] = relationship(back_populates="auth")

    def __repr__(self):
        return f"<CompanyAuth {self.login}>"



class Language(Base):
    code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.active)


    posts: Mapped[List["Post"]] = relationship(back_populates="language")
    notes: Mapped[List["Note"]] = relationship(back_populates="language")
    materials_status: Mapped[List["MaterialsStatus"]] = relationship(back_populates="language")
    help_categories: Mapped[List["HelpCategory"]] = relationship(back_populates="language")

    def __repr__(self):
        return f"<Language {self.code} {self.title}>"

class Company(Base):
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    why_collecting: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    payment: Mapped[str] = mapped_column(String(300), nullable=False, unique=True)
    status: Mapped[StatusEnum] = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.active)

    auth: Mapped["CompanyAuth"] = relationship(back_populates="company", uselist=False)
    help_categories: Mapped[List["HelpCategory"]] = relationship(back_populates="company")
    materials_status: Mapped[List["MaterialsStatus"]] = relationship(back_populates="company")
    help_requests: Mapped[List["HelpRequest"]] = relationship(back_populates="company")
    notes: Mapped[List["Note"]] = relationship(back_populates="company")
    posts: Mapped[List["Post"]] = relationship(back_populates="company")

    def __repr__(self):
        return f"<Company {self.title}>"


class Post(Base):
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"), nullable=False)
    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"), nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[StatusEnum] = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.active)

    company: Mapped["Company"] = relationship(back_populates="posts")
    language: Mapped[Language] = relationship(back_populates="posts")

    def __repr__(self):
        return f"<Post {self.title}>"


class Note(Base):
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"), nullable=False)
    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"), nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    note_type: Mapped[TypeChoices] = mapped_column(SqlEnum(TypeChoices), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
    goal_money: Mapped[float] = mapped_column(Float, nullable=False)
    collected_money: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[StatusEnum] = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.active)

    company: Mapped["Company"] = relationship(back_populates="notes")
    language: Mapped[Language] = relationship(back_populates="notes")

    def __repr__(self):
        return f"<Note {self.title}>"


class MaterialsStatus(Base):
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"), nullable=False)
    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(SqlEnum(StatusEnum), nullable=False)

    company: Mapped["Company"] = relationship(back_populates="materials_status")
    language: Mapped["Language"] = relationship(back_populates="materials_status")
    help_requests: Mapped[List["HelpRequest"]] = relationship(back_populates="materials_status")

    def __repr__(self):
        return f"<MaterialsStatus {self.title}>"


class HelpCategory(Base):
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"), nullable=False)
    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    is_other: Mapped[bool] = mapped_column(Boolean, nullable=False)
    status: Mapped[StatusEnum] = mapped_column(SqlEnum(StatusEnum), nullable=False, default=StatusEnum.active)

    company: Mapped["Company"] = relationship(back_populates="help_categories")
    language: Mapped["Language"] = relationship(back_populates="help_categories")
    help_requests: Mapped[List["HelpRequest"]] = relationship(back_populates="help_category")


    def __repr__(self):
        return f"<HelpCategory {self.title}>"


class HelpRequest(Base):
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"), nullable=False)
    materials_status_id: Mapped[int] = mapped_column(ForeignKey("materials_status.id"), nullable=False)
    help_category_id: Mapped[int] = mapped_column(ForeignKey("help_category.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    surname: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    other_category: Mapped[str] = mapped_column(String(255), nullable=True)
    child_num: Mapped[int] = mapped_column(Integer, nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
    iin: Mapped[str] = mapped_column(String(12), nullable=False)
    help_reason: Mapped[str] = mapped_column(Text, nullable=False)
    received_other_help: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[StatusEnum] = mapped_column(SqlEnum(StatusEnum), nullable=False, default=StatusEnum.active)

    company: Mapped["Company"] = relationship(back_populates="help_requests")
    help_requests_file: Mapped[List["HelpRequestFile"]] = relationship(back_populates="help_request")
    materials_status: Mapped["MaterialsStatus"] = relationship(back_populates="help_requests")
    help_category: Mapped["HelpCategory"] = relationship(back_populates="help_requests")

    def __repr__(self):
        return f"<HelpRequest {self.name} --- {self.surname}>"


class HelpRequestFile(Base):
    help_request_id: Mapped[int] = mapped_column(ForeignKey("help_request.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)

    help_request: Mapped[HelpRequest] = relationship(back_populates="help_requests_file")


    def __repr__(self):
        return f"<HelpRequestFile {self.filename}"







