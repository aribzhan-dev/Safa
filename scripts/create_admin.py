import asyncio
from app.core.db import AsyncSessionLocal
from app.core.security import hash_password
from app.models.admin import Admin


async def create_admin():
    async with AsyncSessionLocal() as session:
        exists = await session.execute(
            Admin.__table__.select().limit(1)
        )
        if exists.first():
            print("Admin already exists")
            return

        admin = Admin(
            login="admin",
            password_hash=hash_password("admin123")
        )

        session.add(admin)
        await session.commit()

        print("Admin created")
        print("Login: admin")
        print("Password: admin123")


if __name__ == "__main__":
    asyncio.run(create_admin())