import json
from typing import Optional, Type, Callable

import asyncpg
from asyncpg import Pool, Connection
from fastapi import Depends

from trainings_app.settings import settings
from trainings_app.repositories.base import BaseRepository
from trainings_app.exceptions.exceptions import UninitializedDatabasePoolError


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


def get_repo(repo_type: Type[BaseRepository]) -> Callable[[Connection], BaseRepository]:
    def inner(conn=Depends(get_conn)) -> BaseRepository:
        return repo_type(conn=conn)

    return inner
