from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from enum import IntEnum
from sqlalchemy import (
    String, Integer, DateTime,
    Enum as SqlEnum, Float,
    ForeignKey, Text, Boolean
)
from datetime import datetime
from typing import List


class StatusEnum(IntEnum):
    active = 0
    inactive = 1
    archived = 2



class TourCompanies(Base):
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    logo: Mapped[str] = mapped_column(String(200), nullable=False)
    comp_name: Mapped[str] = mapped_column(String(50), nullable=False)
    rating: Mapped[float] = mapped_column(Float(), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.active)

    categories: Mapped[List["TourCategories"]] = relationship(back_populates="tour_company")
    guides: Mapped[List["TourGuides"]] = relationship(back_populates="tour_company")
    tours: Mapped[List["Tours"]] = relationship(back_populates="tour_company")

    def __repr__(self):
        return f"<TourCompany -- {self.comp_name}>"



class TourCategories(Base):
    tour_company_id: Mapped[int] = mapped_column(ForeignKey("tour_companies.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.active)

    tour_company: Mapped["TourCompanies"] = relationship(back_populates="categories")
    tours: Mapped[List["Tours"]] = relationship(back_populates="tour_category")

    def __repr__(self):
        return f"<TourCategories -- {self.title}>"



class TourGuides(Base):
    tour_company_id: Mapped[int] = mapped_column(ForeignKey("tour_companies.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    surname: Mapped[str] = mapped_column(String(100), nullable=False)
    about_self: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[float] = mapped_column(Float(), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.active)

    tour_company: Mapped["TourCompanies"] = relationship(back_populates="guides")
    tours: Mapped[List["Tours"]] = relationship(back_populates="tour_guid")

    def __repr__(self):
        return f"<TourGuides -- {self.name} {self.surname}>"



class Tours(Base):
    tour_company_id: Mapped[int] = mapped_column(ForeignKey("tour_companies.id"), nullable=False)
    tour_category_id: Mapped[int] = mapped_column(ForeignKey("tour_categories.id"), nullable=False)
    tour_guid_id: Mapped[int] = mapped_column(ForeignKey("tour_guides.id"), nullable=False)

    image: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float(), nullable=False)
    departure_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    return_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    is_new: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    max_people: Mapped[int] = mapped_column(Integer(), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.active)

    tour_company: Mapped["TourCompanies"] = relationship(back_populates="tours")
    tour_category: Mapped["TourCategories"] = relationship(back_populates="tours")
    tour_guid: Mapped["TourGuides"] = relationship(back_populates="tours")
    files: Mapped[List["TourFiles"]] = relationship(back_populates="tour")

    def __repr__(self):
        return f"<Tours -- {self.location}>"


class TourFiles(Base):
    tour_id: Mapped[int] = mapped_column(ForeignKey("tours.id"), nullable=False)

    file_name: Mapped[str] = mapped_column(String(255), nullable=False)

    tour: Mapped[Tours] = relationship(back_populates="tour_files")

    def __repr__(self):
        return f"<TourFile -- {self.file_name}>"