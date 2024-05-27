# check_postgres_connection.py
import asyncio
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.sql import text
import sys


async def check_connection(database_url):
    try:
        print("DBURL", database_url)
        print("DBURL", database_url[:15])
        print("DBURL", database_url[15:])
        engine = create_async_engine(database_url, echo=True)
        async_session_maker = async_sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )

        async with async_session_maker() as session:
            async with session.begin():
                # Perform a simple query to test the connection
                result = await session.execute(text("SELECT 1"))
                print("Connection successful")

    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    postgres_user = sys.argv[1]
    postgres_password = sys.argv[2]
    postgres_host = sys.argv[3]
    postgres_port = sys.argv[4]
    postgres_db = sys.argv[5]
    database_url = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
    asyncio.run(check_connection(database_url))
