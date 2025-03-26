import asyncio
import pytest
import json
import asyncpg
import pytest_asyncio

from typing import Type, Optional
from asyncpg import Pool, Connection
from pathlib import Path
from yoyo import read_migrations, get_backend

from trainings_app.custom_loggers.test_db import test_db_logger as logger
from trainings_app.exceptions.exceptions import UninitializedDatabasePoolError
from trainings_app.repositories.base import BaseRepository
from trainings_app.settings import settings_test_db

TEST_MIGRATIONS_PATH = Path(__file__).parent.parent / "migrations"
local_test_uri = 'postgresql://test_db_user:test_db_password@localhost:5439/test_db'


def pytest_configure():
    pytest_asyncio.plugin.asyncio_mode = "auto"


def apply_migrations():
    """Read and apply all migrations before tests."""
    backend = get_backend(local_test_uri)
    migrations = read_migrations(str(TEST_MIGRATIONS_PATH))

    with backend.lock():
        unapplied = backend.to_apply(migrations)
        if unapplied:
            logger.info(f"Applying {len(unapplied)} migrations")
            backend.apply_migrations(unapplied)


def rollback_migrations():
    """Read and rollback all migrations after tests."""
    backend = get_backend(local_test_uri)
    migrations = read_migrations(str(TEST_MIGRATIONS_PATH))

    with backend.lock():
        applied = backend.to_rollback(migrations)
        if applied:
            logger.info(f"Rolling back {len(applied)} migrations")
            backend.rollback_migrations(applied)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


class TestAsyncpgPool:
    """
    Connection handler class for the pool with the test database.
    """
    db_pool: Optional[Pool] = None

    @classmethod
    async def setup(cls) -> Pool:
        if cls.db_pool is None:
            try:
                cls.db_pool = await asyncpg.create_pool(
                    dsn=local_test_uri,
                )
            except Exception as e:
                logger.error(f"Postgres initialisation Error: {e}")
                raise UninitializedDatabasePoolError()
        return cls.db_pool

    @classmethod
    async def get_pool(cls) -> Pool:
        if cls.db_pool is None:
            raise UninitializedDatabasePoolError()
        return cls.db_pool

    @classmethod
    async def close_pool(cls):
        if not cls.db_pool:
            raise UninitializedDatabasePoolError()
        await cls.db_pool.close()
        cls.db_pool = None


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db_pool(event_loop) -> Pool:
    """
    Creates a pool for the test database.
    The pool is created before all tests and closed after all tests.
    """
    apply_migrations()
    pool = await TestAsyncpgPool.setup()
    logger.info("Database pool initialized")

    yield pool

    await TestAsyncpgPool.close_pool()
    logger.info("Database pool closed")
    rollback_migrations()


@pytest_asyncio.fixture
async def get_conn(db_pool: Pool) -> Connection:
    """Retrieve the connection from the pool."""
    conn = await db_pool.acquire()
    try:
        await conn.set_type_codec(
            "json",
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog',
        )
        yield conn
    finally:
        await conn.close()


@pytest.fixture
def get_repo(get_conn):
    """Returns a factory function that provides an instance of a repository."""

    def inner(repo_type: Type[BaseRepository]) -> BaseRepository:
        return repo_type(conn=get_conn)

    return inner
