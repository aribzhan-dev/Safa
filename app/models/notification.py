from enum import Enum
from sqlalchemy import DateTime, func, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.models.base import Base


class NotificationTarget(str, Enum):
    sadaqa_company = "sadaqa_company"
    tour_company = "tour_company"
    device = "device"


class Notification(Base):
    __tablename__ = "notifications"
    target: Mapped[NotificationTarget]

    sadaqa_company_id: Mapped[int | None] = mapped_column(
        ForeignKey("companies.id"), nullable=True
    )
    tour_company_id: Mapped[int | None] = mapped_column(
        ForeignKey("tour_companies.id"), nullable=True
    )
    device_id: Mapped[int | None] = mapped_column(
        ForeignKey("devices.id"), nullable=True
    )

    title: Mapped[str]
    body: Mapped[str]

    type: Mapped[str]
    is_read: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            """
            (target = 'sadaqa_company' AND sadaqa_company_id IS NOT NULL AND tour_company_id IS NULL AND device_id IS NULL)
            OR
            (target = 'tour_company' AND tour_company_id IS NOT NULL AND sadaqa_company_id IS NULL AND device_id IS NULL)
            OR
            (target = 'device' AND device_id IS NOT NULL AND sadaqa_company_id IS NULL AND tour_company_id IS NULL)
            """,
            name="notification_target_check"
        ),
    )