import asyncio
from sqlalchemy import select
from app.core.db import AsyncSessionLocal
from app.core.security import hash_password
from app.models.admin import Admin



async def create_admin():
    async with AsyncSessionLocal() as session:
        exists = await session.execute(
            select(Admin).limit(1)
        )
        if exists.scalar_one_or_none():
            print("Admin already exists")
            return

        admin = Admin(
            login="safa_app_az",
            password_hash=hash_password("zair#aribzhan#app")
        )

        session.add(admin)
        await session.commit()

        print("Admin created successfully")
        print("Login: admin")
        print("Password: admin123")


if __name__ == "__main__":
    asyncio.run(create_admin())