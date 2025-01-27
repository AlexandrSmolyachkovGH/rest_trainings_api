import os
import dotenv
from pydantic import BaseModel, SecretStr

dotenv.load_dotenv()


class Settings(BaseModel):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_PORT: int
    POSTGRES_HOST: str
    POSTGRES_DB: str

    @property
    def postgres_dsn(self):
        return f"postgres://" \
               f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}" \
               f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}" \
               f"/{self.POSTGRES_DB}"


DB_CONFIG = {
    "POSTGRES_USER": os.getenv("POSTGRES_USER"),
    "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
    "POSTGRES_DB": os.getenv("POSTGRES_DB"),
    "POSTGRES_HOST": os.getenv("POSTGRES_HOST"),
    "POSTGRES_PORT": os.getenv("POSTGRES_PORT"),
}

settings = Settings(**DB_CONFIG)
