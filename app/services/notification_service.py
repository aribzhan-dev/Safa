# from sqlalchemy.ext.asyncio import AsyncSession
# from app.models.notification import Notification, NotificationTarget
#
#
# async def notify_sadaqa_company(
#     db: AsyncSession,
#     company_id: int,
#     title: str,
#     body: str,
#     type_: str,
# ):
#     notification = Notification(
#         target=NotificationTarget.sadaqa_company,
#         sadaqa_company_id=company_id,
#         title=title,
#         body=body,
#         type=type_,
#     )
#     db.add(notification)
#     await db.commit()
#
#
# async def notify_tour_company(
#     db: AsyncSession,
#     tour_company_id: int,
#     title: str,
#     body: str,
#     type_: str,
# ):
#     notification = Notification(
#         target=NotificationTarget.tour_company,
#         tour_company_id=tour_company_id,
#         title=title,
#         body=body,
#         type=type_,
#     )
#     db.add(notification)
#     await db.commit()
#
#
# async def notify_device(
#     db: AsyncSession,
#     device_id: int,
#     title: str,
#     body: str,
# ):
#     notification = Notification(
#         target=NotificationTarget.device,
#         device_id=device_id,
#         title=title,
#         body=body,
#         type="admin",
#     )
#     db.add(notification)
#     await db.commit()