# check_postgres_connection.py
import asyncio
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.sql import text
import sys


async def check_connection(database_url):
    try:
        print("DBURL", database_url)
        print("DBURL", database_url[:25])
        print("DBURL", database_url[25:])
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
        raise e
        sys.exit(1)

if __name__ == "__main__":
    database_url = sys.argv[1]
    asyncio.run(check_connection(database_url))
