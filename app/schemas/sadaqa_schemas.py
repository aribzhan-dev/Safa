from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from typing import Optional
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

    model_config = ConfigDict(from_attributes=True)


class CompanyBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    why_collecting: str = Field(..., min_length=1)
    image: str = Field(..., max_length=255)
    payment: str = Field(..., min_length=1, max_length=300)


class CompanyCreate(CompanyBase):
    login: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=4)


class CompanyLogin(BaseModel):
    login: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=3, max_length=100)


class CompanyUpdate(BaseModel):
    title: Optional[str] = None
    why_collecting: Optional[str] = None
    image: Optional[str] = None
    payment: Optional[str] = None


class CompanyOut(CompanyBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PostBase(BaseModel):
    language_id: int
    image: str = Field(..., max_length=255)
    title: str = Field(..., min_length=1, max_length=100)
    content: str


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    language_id: Optional[int] = None
    image: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None


class PostOut(PostBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NoteBase(BaseModel):
    language_id: int
    image: str
    note_type: TypeChoices
    title: str
    content: str
    address: str
    goal_money: float
    collected_money: float


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    language_id: Optional[int] = None
    image: Optional[str] = None
    note_type: Optional[TypeChoices] = None
    title: Optional[str] = None
    content: Optional[str] = None
    address: Optional[str] = None
    goal_money: Optional[float] = None
    collected_money: Optional[float] = None


class NoteOut(NoteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MaterialsStatusBase(BaseModel):
    language_id: int
    title: str


class MaterialsStatusCreate(MaterialsStatusBase):
    pass


class MaterialsStatusUpdate(BaseModel):
    language_id: Optional[int] = None
    title: Optional[str] = None


class MaterialsStatusOut(MaterialsStatusBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class HelpCategoryBase(BaseModel):
    language_id: int
    title: str
    is_other: bool


class HelpCategoryCreate(HelpCategoryBase):
    pass


class HelpCategoryUpdate(BaseModel):
    language_id: Optional[int] = None
    title: Optional[str] = None
    is_other: Optional[bool] = None


class HelpCategoryOut(HelpCategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class HelpRequestBase(BaseModel):
    name: str
    surname: str
    age: int
    phone_number: str
    materials_status_id: int
    help_category_id: int
    other_category: Optional[str] = None
    child_num: int
    address: str
    iin: str
    help_reason: str
    received_other_help: bool

    @field_validator("phone_number")
    def validate_phone(cls, v):
        if not v.replace("+", "").replace("-", "").isdigit():
            raise ValueError("Phone number must contain only digits, + or -")
        return v

    @field_validator("iin")
    def validate_iin(cls, v):
        if not v.isdigit() or len(v) != 12:
            raise ValueError("IIN must be exactly 12 digits")
        return v


class HelpRequestCreate(HelpRequestBase):
    pass


class HelpRequestUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    age: Optional[int] = None
    phone_number: Optional[str] = None
    materials_status_id: Optional[int] = None
    help_category_id: Optional[int] = None
    other_category: Optional[str] = None
    child_num: Optional[int] = None
    address: Optional[str] = None
    iin: Optional[str] = None
    help_reason: Optional[str] = None
    received_other_help: Optional[bool] = None


class HelpRequestOut(HelpRequestBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HelpRequestFileBase(BaseModel):
    filename: str


class HelpRequestFileCreate(HelpRequestFileBase):
    pass


class HelpRequestFileOut(HelpRequestFileBase):
    id: int
    help_request_id: int

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
