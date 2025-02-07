import json
from typing import Type

import pytest
import asyncpg
from asyncpg import Connection

from apply_migrations_test_db import migrate_test_db
from trainings_app.custom_loggers.main import main_logger
from trainings_app.db.connection import AsyncpgPool
from trainings_app.exceptions.exceptions import UninitializedDatabasePoolError
from trainings_app.repositories.base import BaseRepository
from trainings_app.settings import settings_test_db



class TestAsyncpgPool(AsyncpgPool):
    @classmethod
    async def setup(cls) -> None:
        """
        Initializes the connection pool for the test database.
        """
        try:
            cls.db_pool = await asyncpg.create_pool(settings_test_db.postgres_dsn)
        except UninitializedDatabasePoolError as e:
            main_logger.error(f"Postgres initialisation Error: {e}")
            raise UninitializedDatabasePoolError()


@pytest.fixture(scope="session", autouse=True)
async def db_pool() -> None:
    """
    Creates a pool for the test database.
    The pool is created before all tests and closed after all tests.
    """
    await TestAsyncpgPool.setup()
    yield
    await TestAsyncpgPool.close_pool()


@pytest.fixture
async def get_conn() -> Connection:
    """
    Provides a connection to the test database.
    """
    pool = await TestAsyncpgPool.get_pool()
    async with pool.acquire() as conn:
        await conn.set_type_codec(
            "json",
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )
        yield conn


@pytest.fixture
def get_repo(get_conn):
    """
    Takes a repository class inherited from BaseRepository.
    Returns an instance of the repository with a pre-configured connection.
    """

    def inner(repo_type: Type[BaseRepository]) -> BaseRepository:
        return repo_type(conn=get_conn)

    return inner
