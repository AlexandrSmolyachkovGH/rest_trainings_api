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
    # PAYMENT SERVICE
    PAYMENT_SERVICE_HOST: str

    @property
    def postgres_dsn(self):
        return f"postgres://" \
               f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}" \
               f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}" \
               f"/{self.POSTGRES_DB}"

    @property
    def postgres_dsn_celery(self):
        return f"db+postgresql://" \
               f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}" \
               f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/" \
               f"{self.POSTGRES_DB}"

    @property
    def payment_service_post_url(self):
        return f"{self.PAYMENT_SERVICE_HOST}/payments/"

    @property
    def payment_service_pay_page(self):
        return f"{self.PAYMENT_SERVICE_HOST}/pay-page/"


DB_CONFIG = {
    "POSTGRES_USER": os.getenv("POSTGRES_USER"),
    "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
    "POSTGRES_DB": os.getenv("POSTGRES_DB"),
    "POSTGRES_HOST": os.getenv("POSTGRES_HOST"),
    "POSTGRES_PORT": os.getenv("POSTGRES_PORT"),
}
TEST_DB_CONFIG = {
    "POSTGRES_USER": os.getenv("TEST_POSTGRES_USER"),
    "POSTGRES_PASSWORD": os.getenv("TEST_POSTGRES_PASSWORD"),
    "POSTGRES_DB": os.getenv("TEST_POSTGRES_DB"),
    "POSTGRES_HOST": os.getenv("TEST_POSTGRES_HOST"),
    "POSTGRES_PORT": os.getenv("TEST_POSTGRES_PORT"),
}
PAYMENT_SERVICE_CONFIG = {
    "PAYMENT_SERVICE_HOST": os.getenv("PAYMENT_SERVICE_HOST"),
}

settings = Settings(**DB_CONFIG, **PAYMENT_SERVICE_CONFIG)
settings_test_db = Settings(**TEST_DB_CONFIG, **PAYMENT_SERVICE_CONFIG)
