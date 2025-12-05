from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
from enum import Enum, IntEnum


class TypeChoices(str, Enum):
    normal = "Обычный"
    medium = "Средний"
    urgent = "Срочный"
    very_urgent = "Очень срочный"


class StatusEnum(IntEnum):
    active = 0
    inactive = 1
    archived = 2



class LanguageBase(BaseModel):
    code: str = Field(..., min_length=2, max_length=10)
    title: str = Field(..., min_length=1, max_length=200)
    


class LanguageCreate(LanguageBase):
    pass


class LanguageOut(LanguageBase):
    id: int

    class Config:
        from_attributes = True



class CompanyBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    why_collecting: str = Field(..., min_length=1)
    image: str = Field(..., max_length=255)
    


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    why_collecting: Optional[str] = None
    image: Optional[str] = Field(None, max_length=255)
    


class CompanyOut(CompanyBase):
    id: int

    class Config:
        from_attributes = True




class PostBase(BaseModel):
    language_id: int
    image: str = Field(..., max_length=255)
    title: str = Field(..., min_length=1, max_length=100)
    content: str
    


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    language_id: Optional[int] = None
    image: Optional[str] = Field(None, max_length=255)
    title: Optional[str] = Field(None, max_length=100, min_length=1)
    content: Optional[str] = None
    


class PostOut(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True




class NoteBase(BaseModel):
    language_id: int
    image: str = Field(..., max_length=255)
    note_type: TypeChoices
    title: str = Field(..., min_length=1, max_length=100)
    content: str
    address: str = Field(..., min_length=1, max_length=200)
    goal_money: float
    collected_money: float
    


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    language_id: Optional[int] = None
    image: Optional[str] = Field(None, max_length=255)
    note_type: Optional[TypeChoices] = None
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = None
    address: Optional[str] = Field(None, min_length=1, max_length=200)
    goal_money: Optional[float] = None
    collected_money: Optional[float] = None
    


class NoteOut(NoteBase):
    id: int

    class Config:
        from_attributes = True



class MaterialsStatusBase(BaseModel):
    language_id: int
    title: str = Field(..., min_length=1, max_length=100)


class MaterialsStatusCreate(MaterialsStatusBase):
    pass


class MaterialsStatusUpdate(BaseModel):
    language_id: Optional[int] = None
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    


class MaterialsStatusOut(MaterialsStatusBase):
    id: int

    class Config:
        from_attributes = True



class HelpCategoryBase(BaseModel):
    language_id: int
    title: str = Field(..., min_length=1, max_length=100)
    is_other: bool
    


class HelpCategoryCreate(HelpCategoryBase):
    pass


class HelpCategoryUpdate(BaseModel):
    language_id: Optional[int] = None
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    is_other: Optional[bool] = None
    


class HelpCategoryOut(HelpCategoryBase):
    id: int

    class Config:
        from_attributes = True



class HelpRequestBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    surname: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., gt=0)
    phone_number: str = Field(..., min_length=10, max_length=20)
    materials_status_id: int
    help_category_id: int
    other_category: Optional[str] = Field(None, max_length=255)
    child_num: int = Field(..., ge=0)
    address: str = Field(..., min_length=1, max_length=200)
    iin: str = Field(..., min_length=12, max_length=12)
    help_reason: str = Field(..., min_length=5)
    received_other_help: bool
    


    @field_validator("phone_number")
    def validate_phone(cls, v):
        if not v.replace("+", "").replace("-", "").isdigit():
            raise ValueError("Phone number must contain only digits, + or -")
        return v

    @field_validator("iin")
    def validate_iin(cls, v):
        if not v.isdigit():
            raise ValueError("IIN must contain only digits")
        if len(v) != 12:
            raise ValueError("IIN must be exactly 12 digits")
        return v


class HelpRequestCreate(HelpRequestBase):
    pass


class HelpRequestUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    surname: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = None
    phone_number: Optional[str] = Field(None, min_length=10, max_length=20)
    materials_status_id: Optional[int] = None
    help_category_id: Optional[int] = None
    other_category: Optional[str] = Field(None, max_length=255)
    child_num: Optional[int] = None
    address: Optional[str] = Field(None, min_length=1, max_length=200)
    iin: Optional[str] = Field(None, min_length=12, max_length=12)
    help_reason: Optional[str] = None
    received_other_help: Optional[bool] = None

    @field_validator("phone_number")
    def validate_phone(cls, v):
        if v is None:
            return v
        if not v.replace("+", "").replace("-", "").isdigit():
            raise ValueError("Phone number must contain only digits, + or -")
        return v

    @field_validator("iin")
    def validate_iin(cls, v):
        if v is None:
            return v
        if not v.isdigit():
            raise ValueError("IIN must contain only digits")
        if len(v) != 12:
            raise ValueError("IIN must be exactly 12 digits")
        return v


class HelpRequestOut(HelpRequestBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True



class HelpRequestFileBase(BaseModel):
    help_request_id: int
    filename: str = Field(..., max_length=255)


class HelpRequestFileCreate(HelpRequestFileBase):
    pass

class HelpRequestFileOut(HelpRequestFileBase):
    id: int

    class Config:
        from_attributes = True