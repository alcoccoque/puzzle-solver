# check_postgres_connection.py
import asyncio
import asyncpg
import sys

async def check_connection(database_url):
    try:
        conn = await asyncpg.connect(database_url)
        await conn.close()
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
    database_url = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@test-{postgres_host}:{postgres_port}/{postgres_db}"
    asyncio.run(check_connection(database_url))
