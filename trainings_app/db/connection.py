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

pool = None


async def connect_to_db():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(**DB_CONFIG, **EXTRA_CONFIG)
        print("DB: Created the pool")


async def close_db():
    global pool
    if pool:
        await pool.close()
        pool = None
        print("DB: Closed the pool")


@asynccontextmanager
async def get_db():
    global pool
    if pool is None:
        raise RuntimeError("DB: No active pool")
    async with pool.acquire() as conn:
        yield conn
