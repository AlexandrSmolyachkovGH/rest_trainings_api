import os
import asyncpg
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import Depends
from trainings_app.repositories.base import BaseRepository

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


async def get_conn():
    async with asyncpg.create_pool(**DB_CONFIG, **EXTRA_CONFIG) as pool:
        async with pool.acquire() as conn:
            yield conn


def get_repo(repo_type):
    async def inner(db=Depends(get_conn)):
        return repo_type(db)

    return inner
