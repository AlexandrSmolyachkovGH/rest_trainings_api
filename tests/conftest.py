import asyncio

import pytest
import asyncpg
from typing import Type

import pytest_asyncio
from asyncpg import Connection
from pathlib import Path
from yoyo import read_migrations, get_backend

from trainings_app.custom_loggers.test_db import test_db_logger as logger
from trainings_app.db.connection import AsyncpgPool
from trainings_app.exceptions.exceptions import UninitializedDatabasePoolError
from trainings_app.repositories.base import BaseRepository
from trainings_app.settings import settings_test_db
import json

TEST_MIGRATIONS_PATH = Path("../migrations").resolve()
local_test_uri = 'postgresql://test_db_user:test_db_password@localhost:5439/test_db'

import pytest_asyncio


def pytest_configure():
    pytest_asyncio.plugin.asyncio_mode = "auto"


@pytest.fixture(scope='session', autouse=True)
def migrate_test_db():
    # backend = get_backend(settings_test_db.postgres_dsn)
    backend = get_backend(local_test_uri)
    migrations = read_migrations(str(TEST_MIGRATIONS_PATH))

    with backend.lock():
        unapplied = backend.to_apply(migrations)
        if unapplied:
            logger.info("Applying migrations for the test db.")
            backend.apply_migrations(unapplied)
            logger.info("Migrations applied successfully.")

    yield

    logger.info("Rolling back migrations for the test db.")
    applied = backend.to_rollback(migrations)
    if applied:
        backend.rollback_migrations(applied)
        logger.info("Migrations rolled back successfully.")


@pytest_asyncio.fixture(scope="session")
async def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


class TestAsyncpgPool(AsyncpgPool):
    @classmethod
    async def setup(cls) -> None:
        """
        Initializes the connection pool for the test database.
        """
        try:
            # cls.db_pool = await asyncpg.create_pool(settings_test_db.postgres_dsn)
            cls.db_pool = await asyncpg.create_pool(local_test_uri)
        except UninitializedDatabasePoolError as e:
            logger.error(f"Postgres initialisation Error: {e}")
            raise UninitializedDatabasePoolError()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db_pool() -> None:
    """
    Creates a pool for the test database.
    The pool is created before all tests and closed after all tests.
    """
    await TestAsyncpgPool.setup()
    yield
    await TestAsyncpgPool.close_pool()


@pytest_asyncio.fixture
async def get_conn() -> Connection:
    """
    Provides a connection to the test database.
    """
    pool = await TestAsyncpgPool.get_pool()
    conn = await pool.acquire()
    await conn.set_type_codec(
        "json",
        encoder=json.dumps,
        decoder=json.loads,
        schema='pg_catalog'
    )
    yield conn
    await pool.release(conn)


@pytest_asyncio.fixture
async def get_repo(get_conn):
    """
    Takes a repository class inherited from BaseRepository.
    Returns an instance of the repository with a pre-configured connection.
    """

    conn = await get_conn

    def inner(repo_type: Type[BaseRepository]) -> BaseRepository:
        return repo_type(conn=conn)

    return inner
