from yoyo import read_migrations, get_backend
from trainings_app.settings import settings
from pathlib import Path


MIGRATIONS_PATH = Path("D:/fastapi_projects/rest_trainings_api/migrations").resolve()

def migrate():
    print(f'[migration] -- APPLY MIGRATION [{settings.postgres_dsn}] --')
    backend = get_backend(settings.postgres_dsn)
    migrations = read_migrations(str(MIGRATIONS_PATH))

    with backend.lock():
        # Apply any outstanding migrations
        backend.apply_migrations(backend.to_apply(migrations))

    print("[migration] -- MIGRATE SUCCESS --")


def main():
    migrate()


if __name__ == '__main__':
    main()
