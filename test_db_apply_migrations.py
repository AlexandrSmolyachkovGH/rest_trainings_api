from pathlib import Path

import pytest
from yoyo import read_migrations, get_backend

from trainings_app.custom_loggers.test_db_init import test_db_init_logger as logger
from trainings_app.settings import settings_test_db

TEST_MIGRATIONS_PATH = Path("migrations").resolve()


@pytest.fixture(scope='session', autouse=True)
def migrate_test_db():
    backend = get_backend(settings_test_db)
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

