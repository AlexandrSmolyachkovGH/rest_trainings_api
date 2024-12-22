from dotenv import load_dotenv
import os
from yoyo import read_migrations, get_backend

load_dotenv()

db_uri = os.getenv("DB_URI")
backend = get_backend(db_uri)
migrations = read_migrations('migrations')
with backend.lock():
    backend.apply_migrations(backend.to_apply(migrations))
    print("Migrations have been successfully applied.")
