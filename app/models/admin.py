from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Admin(Base):
    __tablename__ = "admins"

    login: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]

    is_active: Mapped[bool] = mapped_column(default=True)