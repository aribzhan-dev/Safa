from app.models.base import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime

class Device(Base):
    __tablename__ = "devices"
    device_uid: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        comment="UUID from mobile app"
    )
    platform: Mapped[str] = mapped_column(
        String(20),
        comment="ios | android"
    )
    push_token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )