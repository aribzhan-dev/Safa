from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
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
    pass


class TourCompanyUpdate(BaseModel):
    logo: Optional[str] = Field(None, max_length=200)
    comp_name: Optional[str] = Field(None, min_length=1, max_length=50)
    rating: Optional[float] = Field(None, ge=0, le=5)


class TourCompanyOut(TourCompanyBase):
    id: int

    class Config:
        from_attributes = True




class TourCategoryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)


class TourCategoryCreate(TourCategoryBase):
    pass


class TourCategoryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)


class TourCategoryOut(TourCategoryBase):
    id: int

    class Config:
        from_attributes = True




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
    ratign: Optional[float] = Field(None, ge=0, le=5)

class TourGuideOut(TourGuideBase):
    id: int

    class Config:
        from_attributes = True



class TourBase(BaseModel):
    tour_company_id: int
    tour_category_id: int
    tour_guid_id: int

    image: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., ge=0)
    departure_date: datetime
    return_date: datetime
    is_new: bool
    max_people: int = Field(..., ge=1)
    location: str = Field(..., min_length=1, max_length=255)

    @field_validator("return_date")
    def validate_return_date(cls, v, values):
        start = values.get("departure_date")
        if start and v < start:
            raise ValueError("return_date must be later than departure_date")
        return v


class TourCreate(TourBase):
    pass


class TourUpdate(BaseModel):
    tour_company_id: Optional[int] = None
    tour_category_id: Optional[int] = None
    tour_guid_id: Optional[int] = None

    image: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[float] = Field(None, ge=0)
    departure_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    is_new: Optional[bool] = None
    max_people: Optional[int] = Field(None, ge=1)
    location: Optional[str] = Field(None, min_length=1, max_length=255)

    @field_validator("return_date")
    def validate_return_update(cls, v, values):
        start = values.get("departure_date")
        if start and v and v < start:
            raise ValueError("return_date must be later than departure_date")
        return v


class TourOut(TourBase):
    id: int

    class Config:
        from_attributes = True