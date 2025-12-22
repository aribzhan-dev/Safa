from pydantic import BaseModel, Field, field_validator, ConfigDict, model_validator
from datetime import datetime
from typing import Optional
from enum import IntEnum


class StatusEnum(IntEnum):
    active = 0
    inactive = 1
    archived = 2


class TourCompanyBase(BaseModel):
    logo: str = Field(..., max_length=200)
    comp_name: str = Field(..., min_length=1, max_length=50)
    rating: float = Field(..., ge=0, le=5)


class TourCompanyCreate(TourCompanyBase):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)


class TourCompanyUpdate(BaseModel):
    logo: Optional[str] = Field(None, max_length=200)
    comp_name: Optional[str] = Field(None, min_length=1, max_length=50)
    rating: Optional[float] = Field(None, ge=0, le=5)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=6, max_length=100)


class TourCompanyOut(TourCompanyBase):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class TourCompanyLogin(BaseModel):
    username: str
    password: str


class TourCategoryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)


class TourCategoryCreate(TourCategoryBase):
    pass


class TourCategoryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)


class TourCategoryOut(TourCategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TourGuideBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    surname: str = Field(..., min_length=1, max_length=100)
    about_self: str = Field(..., min_length=5)
    rating: float = Field(..., ge=0, le=5)


class TourGuideCreate(TourGuideBase):
    pass


class TourGuideUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    surname: Optional[str] = Field(None, min_length=1, max_length=100)
    about_self: Optional[str] = Field(None, min_length=5)
    rating: Optional[float] = Field(None, ge=0, le=5)


class TourGuideOut(TourGuideBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TourBase(BaseModel):
    tour_category_id: int
    tour_guid_id: int

    image: str = Field(..., max_length=255)
    price: float = Field(..., ge=0)
    departure_date: datetime
    return_date: datetime
    duration: int = Field(..., ge=0)
    is_new: bool
    max_people: int = Field(..., ge=1)
    location: str = Field(..., min_length=1, max_length=255)

    @model_validator(mode="after")
    def check_dates(self):
        if self.return_date < self.departure_date:
            raise ValueError("return_date must be after departure_date")
        return self


class TourCreate(TourBase):
    pass


class TourUpdate(BaseModel):
    tour_category_id: Optional[int] = None
    tour_guid_id: Optional[int] = None

    image: Optional[str] = Field(None, max_length=255)
    price: Optional[float] = Field(None, ge=0)
    departure_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    duration: Optional[int] = Field(None, ge=0)
    is_new: Optional[bool] = None
    max_people: Optional[int] = Field(None, ge=1)
    location: Optional[str] = Field(None, min_length=1, max_length=255)

    @model_validator(mode="after")
    def check_dates(self):
        if self.departure_date and self.return_date:
            if self.return_date < self.departure_date:
                raise ValueError(
                    "return_date must be after departure_date"
                )
        return self


class TourOut(TourBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TourFileBase(BaseModel):
    file_name: str


class TourFileCreate(TourFileBase):
    pass


class TourFileOut(TourFileBase):
    id: int
    tour_id: int

    model_config = ConfigDict(from_attributes=True)


class BookingBase(BaseModel):
    person_number: int
    name: str
    surname: str
    patronymic: Optional[str] = None

    phone: str
    email: Optional[str] = None

    passport_number: str
    date_of_birth: datetime


class BookingCreate(BookingBase):
    tour_id: int


class BookingUpdate(BaseModel):
    secret_code: str

    person_number: Optional[int] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None

    phone: Optional[str] = None
    email: Optional[str] = None
    passport_number: Optional[str] = None
    date_of_birth: Optional[datetime] = None


class BookingOut(BookingBase):
    id: int
    tour_id: int
    secret_code: str
    booking_date: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshRequest(BaseModel):
    refresh_token: str