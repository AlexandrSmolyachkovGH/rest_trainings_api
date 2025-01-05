import logging
from yoyo import read_migrations, get_backend
from trainings_app.settings import settings
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)

MIGRATIONS_PATH = Path("migrations").resolve()


def migrate():
    print(f'[migration] -- APPLY MIGRATION [{settings.postgres_dsn}] --')
    backend = get_backend(settings.postgres_dsn)
    migrations = read_migrations(str(MIGRATIONS_PATH))

    with backend.lock():
        unapplied = backend.to_apply(migrations)
        logging.debug(f'[migration] -- UNAPPLIED MIGRATIONS: {[m.id for m in unapplied]}')

        if unapplied:
            backend.apply_migrations(unapplied)
            logging.debug(f'[migration] -- ALL MIGRATIONS APPLIED SUCCESSFULLY')

    print("[migration] -- MIGRATE SUCCESS --")



if __name__ == '__main__':
    migrate()
