import json
# import os
from typing import Optional, Type

import asyncpg
from asyncpg import Pool, Connection
from fastapi import Depends
# from dotenv import load_dotenv

from trainings_app.settings import settings
from trainings_app.repositories.base import BaseRepository
from trainings_app.exceptions.exceptions import UninitializedDatabasePoolError


# load_dotenv()
#
# DB_CONFIG = {
#     "user": os.getenv("POSTGRES_USER"),
#     "password": os.getenv("POSTGRES_PASSWORD"),
#     "database": os.getenv("POSTGRES_DB"),
#     "host": os.getenv("POSTGRES_HOST"),
#     "port": os.getenv("POSTGRES_PORT"),
# }
#
# EXTRA_CONFIG = {
#     "max_size": 10,
#     "min_size": 1
# }
#
#
# async def get_conn():
#     async with asyncpg.create_pool(**DB_CONFIG, **EXTRA_CONFIG) as pool:
#         async with pool.acquire() as conn:
#             yield conn
#
#
# def get_repo(repo_type):
#     async def inner(db=Depends(get_conn)):
#         return repo_type(db)
#
#     return inner


class AsyncpgPool:
    db_pool: Optional[Pool] = None

    @classmethod
    async def setup(cls) -> None:
        cls.db_pool = await asyncpg.create_pool(settings.postgres_dsn)

    @classmethod
    async def get_pool(cls) -> Pool:
        if not cls.db_pool:
            raise UninitializedDatabasePoolError()
        return cls.db_pool

    @classmethod
    async def close_pool(cls) -> None:
        if not cls.db_pool:
            raise UninitializedDatabasePoolError()
        await cls.db_pool.close()


async def get_conn(pool: Pool = Depends(AsyncpgPool.get_pool)) -> Connection:
    async with pool.acquire() as conn:
        await conn.set_type_codec(
            "json",
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )
        yield conn


def get_repo(repo_type: Type[BaseRepository]) -> BaseRepository:
    def inner(conn=Depends(get_conn)):
        return repo_type(conn=conn)

    return inner
