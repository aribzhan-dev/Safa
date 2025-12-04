from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from sqlalchemy.sql import func
from enum import Enum, IntEnum
from sqlalchemy import (
    String, Integer, DateTime,
    Enum as SqlEnum, Float,
    ForeignKey, Text
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



class Language(Base):
    code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.active)

    companies: Mapped[List["Company"]] = relationship(back_populates="language")
    posts: Mapped[List["Post"]] = relationship(back_populates="language")
    notes: Mapped[List["Note"]] = relationship(back_populates="language")


    def __repr__(self):
        return f"<Language {self.code} {self.title}>"

class Company(Base):
    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"), nullable=False)
    language: Mapped[Language] = relationship(back_populates="companies")
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    why_collecting: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.active)

    def __repr__(self):
        return f"<Company {self.title}>"


class Post(Base):
    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"), nullable=False)
    language: Mapped[Language] = relationship(back_populates="posts")
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[StatusEnum] = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.active)

    def __repr__(self):
        return f"<Post {self.title}>"


class Note(Base):
    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"), nullable=False)
    language: Mapped[Language] = relationship(back_populates="notes")
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    note_type: Mapped[TypeChoices] = mapped_column(SqlEnum(TypeChoices), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
    goal_money: Mapped[float] = mapped_column(Float, nullable=False)
    collected_money: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[StatusEnum] = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.active)

    def __repr__(self):
        return f"<Note {self.title}>"





