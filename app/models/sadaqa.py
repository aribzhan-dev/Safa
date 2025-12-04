from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, Enum as SqlEnum, Float
from sqlalchemy import ForeignKey
from app.models.base import Base
from datetime import datetime
from enum import Enum


class TypeChoices(str, Enum):
    normal = "Обычный"
    medium = "Средний"
    urgent = "Срочный"
    very_urgent = "Очень срочный"



class Language(Base):
    code: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String, nullable=False)


    def __repr__(self):
        return f"<Language {self.code} {self.title}>"

class Company(Base):
    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"), nullable=False)
    language: Mapped[Language] = relationship()
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    why_collecting: Mapped[str] = mapped_column(String, nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self):
        return f"<Company {self.title}>"


class Post(Base):
    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"), nullable=False)
    language: Mapped[Language] = relationship()
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    status: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self):
        return f"<Post {self.title}>"


class Note(Base):
    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"), nullable=False)
    language: Mapped[Language] = relationship()
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    type_choices: Mapped[TypeChoices] = mapped_column(SqlEnum(TypeChoices), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    goal_money: Mapped[float] = mapped_column(Float, nullable=False)
    collected_money: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self):
        return f"<Note {self.title}>"





