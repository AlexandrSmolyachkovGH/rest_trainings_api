import asyncpg
import asyncio
import os

DB_NAME = os.getenv('TEST_POSTGRES_DB')
DB_USER = os.getenv('TEST_POSTGRES_USER')
DB_PASSWORD = os.getenv('TEST_POSTGRES_PASSWORD')
DB_HOST = os.getenv('TEST_POSTGRES_HOST')
DB_PORT = os.getenv('TEST_POSTGRES_PORT')


async def create_test_database():
    """Create database for tests if not exists."""
    conn = await asyncpg.connect(user=DB_USER, password=DB_PASSWORD, database="postgres", host=DB_HOST, port=DB_PORT)
    db_exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", DB_NAME)
    if not db_exists:
        await conn.execute(f'CREATE DATABASE {DB_NAME}')
    await conn.close()


if __name__ == "__main__":
    asyncio.run(create_test_database())
