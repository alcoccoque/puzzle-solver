"""Async session."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import prod_db_settings

print("\n\n\n\n\n\n")
print(prod_db_settings.DATABASE_URL)
print("\n\n\n\n\n\n")
engine = create_async_engine(prod_db_settings.DATABASE_URL)
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async session."""
    async with async_session_maker() as session:
        yield session
