import os
import asyncpg
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "database": os.getenv("POSTGRES_DB"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
}


EXTRA_CONFIG = {
    "max_size": 10,
    "min_size": 1
}
print("DB_CONFIG:", DB_CONFIG)

async def connect_to_db():
    return await asyncpg.create_pool(**DB_CONFIG, **EXTRA_CONFIG)


@asynccontextmanager
async def get_db():
    pool = await connect_to_db()
    async with pool.acquire() as conn:
        yield conn
    await pool.close()
