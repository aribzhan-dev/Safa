from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from enum import IntEnum
from sqlalchemy import (
    String, Integer, DateTime,
    Enum as SqlEnum, Float,
    ForeignKey, Text, Boolean, func
)
from datetime import datetime
from typing import List


class StatusEnum(IntEnum):
    active = 0
    inactive = 1
    archived = 2



class TourCompanies(Base):
    __tablename__ = "tour_companies"
    username = mapped_column(String(50), unique=True, nullable=False)
    password_hash = mapped_column(String(255), nullable=False)

    logo = mapped_column(String(200), nullable=False)
    comp_name = mapped_column(String(50), nullable=False)
    rating = mapped_column(Float(), nullable=False)
    status = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.active)

    categories = relationship("TourCategories", back_populates="tour_company")
    guides = relationship("TourGuides", back_populates="tour_company")
    tours = relationship("Tours", back_populates="tour_company")

    def __repr__(self):
        return f"<TourCompany -- {self.comp_name}>"



class TourCategories(Base):
    __tablename__ = "tour_categories"
    tour_company_id = mapped_column(ForeignKey("tour_companies.id"), nullable=False)

    title = mapped_column(String(200), nullable=False)
    status = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.active)

    tour_company = relationship("TourCompanies", back_populates="categories")
    tours = relationship("Tours", back_populates="tour_category")

    def __repr__(self):
        return f"<TourCategories -- {self.title}>"



class TourGuides(Base):
    __tablename__ = "tour_guides"
    tour_company_id = mapped_column(ForeignKey("tour_companies.id"), nullable=False)

    name = mapped_column(String(100), nullable=False)
    surname = mapped_column(String(100), nullable=False)
    about_self = mapped_column(Text, nullable=False)
    rating = mapped_column(Float(), nullable=False)
    status = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.active)

    tour_company = relationship("TourCompanies", back_populates="guides")
    tours = relationship("Tours", back_populates="tour_guid")

    def __repr__(self):
        return f"<TourGuides -- {self.name} {self.surname}>"



class Tours(Base):
    __tablename__ = "tours"

    tour_company_id = mapped_column(ForeignKey("tour_companies.id"), nullable=False)
    tour_category_id = mapped_column(ForeignKey("tour_categories.id"), nullable=False)
    tour_guid_id = mapped_column(ForeignKey("tour_guides.id"), nullable=False)

    image = mapped_column(String(255), nullable=False)
    price = mapped_column(Float(), nullable=False)
    departure_date = mapped_column(DateTime(), nullable=False)
    return_date = mapped_column(DateTime(), nullable=False)
    duration = mapped_column(Integer(), nullable=False)
    is_new = mapped_column(Boolean(), nullable=False)
    max_people = mapped_column(Integer(), nullable=False)
    location = mapped_column(String(255), nullable=False)
    status = mapped_column(SqlEnum(StatusEnum), default=StatusEnum.active)

    tour_company = relationship("TourCompanies", back_populates="tours")
    tour_category = relationship("TourCategories", back_populates="tours")
    tour_guid = relationship("TourGuides", back_populates="tours")
    files = relationship("TourFiles", back_populates="tour")
    booking = relationship("BookingTour", back_populates="tour")

    def __repr__(self):
        return f"<Tours -- {self.location}>"


class TourFiles(Base):
    tour_id = mapped_column(ForeignKey("tours.id"), nullable=False)
    file_name = mapped_column(String(255), nullable=False)

    tour = relationship("Tours", back_populates="files")

    def __repr__(self):
        return f"<TourFile -- {self.file_name}>"



class BookingTour(Base):
    tour_id = mapped_column(ForeignKey("tours.id"), nullable=False)

    person_number = mapped_column(Integer(), nullable=False)
    name = mapped_column(String(255), nullable=False)
    surname = mapped_column(String(255), nullable=False)
    patronymic = mapped_column(String(255), nullable=True)
    phone = mapped_column(String(255), nullable=False)
    email = mapped_column(String(255), nullable=True)
    passport_number = mapped_column(String(10), nullable=False)
    date_of_birth = mapped_column(DateTime(), nullable=False)
    booking_date = mapped_column(DateTime(), nullable=False, server_default=func.now())
    secret_code = mapped_column(String(20), nullable=False)

    tour = relationship("Tours", back_populates="booking")

    def __repr__(self):
        return f"<BookingTour -- {self.name} -- {self.surname}>"

