"""Async session."""
import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import prod_db_settings

print("TEST")
print("POSTGRES_USER=", os.getenv("POSTGRES_USER"))
print("POSTGRES_PASSWORD=", os.getenv("POSTGRES_PASSWORD"))
print("POSTGRES_HOST=", os.getenv("POSTGRES_HOST"))
print("POSTGRES_PORT=", os.getenv("POSTGRES_PORT"))
print("POSTGRES_DB=", os.getenv("POSTGRES_DB"))
print("DATABASE_URL=", f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@test-{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}")
engine = create_async_engine(prod_db_settings.DATABASE_URL)
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async session."""
    async with async_session_maker() as session:
        yield session
