import os

import dotenv
from pydantic import BaseModel, SecretStr

dotenv.load_dotenv()


class Settings(BaseModel):
    # POSTGRES
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_PORT: int
    POSTGRES_HOST: str
    POSTGRES_DB: str
    # PAYMENT SERVICE
    PAYMENT_SERVICE_HOST: str
    # RABBIT MQ REPORT
    REP_RABBIT_VHOST: str
    REP_RABBIT_USER: str
    REP_RABBIT_PASS: SecretStr
    REP_RABBIT_HOST: str
    # RABBIT MQ PAYMENT
    PAY_RABBIT_USER: str
    PAY_RABBIT_PASSWORD: SecretStr
    PAY_RABBIT_HOST: str
    PAY_RABBIT_PORT: str

    @property
    def postgres_dsn(self):
        return f"postgres://" \
               f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}" \
               f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}" \
               f"/{self.POSTGRES_DB}"

    @property
    def payment_service_post_url(self):
        return f"{self.PAYMENT_SERVICE_HOST}/payments/"

    @property
    def payment_service_pay_page(self):
        return f"{self.PAYMENT_SERVICE_HOST}/pay-page/"

    @property
    def rabbitmq_dsn(self):
        return f"pyamqp://" \
               f"{self.REP_RABBIT_USER}:{self.REP_RABBIT_PASS.get_secret_value()}@" \
               f"{self.REP_RABBIT_HOST}/{self.REP_RABBIT_VHOST}"

    @property
    def rabbitmq_payment_dsn(self):
        return f"pyamqp://" \
               f"{self.PAY_RABBIT_USER}:{self.PAY_RABBIT_PASSWORD.get_secret_value()}@" \
               f"{self.PAY_RABBIT_HOST}/{self.PAY_RABBIT_PORT}"


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
RABBITMQ_REPORT = {
    'REP_RABBIT_VHOST': os.getenv('RABBITMQ_DEFAULT_VHOST', '/'),
    'REP_RABBIT_USER': os.getenv('RABBITMQ_DEFAULT_USER', 'guest'),
    'REP_RABBIT_PASS': SecretStr(os.getenv('RABBITMQ_DEFAULT_PASS', 'guest')),
    'REP_RABBIT_HOST': os.getenv('RABBITMQ_HOST', 'localhost'),
}
RABBITMQ_PAYMENT = {
    'PAY_RABBIT_USER': os.getenv("PAYMENT_RABBITMQ_USER"),
    'PAY_RABBIT_PASSWORD': SecretStr(os.getenv("PAYMENT_RABBITMQ_PASS")),
    'PAY_RABBIT_HOST': os.getenv("PAYMENT_RABBITMQ_SERVER_IP"),
    'PAY_RABBIT_PORT': os.getenv("PAYMENT_RABBITMQ_AMQP_PORT"),
}

settings = Settings(**DB_CONFIG, **PAYMENT_SERVICE_CONFIG, **RABBITMQ_REPORT, **RABBITMQ_PAYMENT)
settings_test_db = Settings(**TEST_DB_CONFIG, **PAYMENT_SERVICE_CONFIG, **RABBITMQ_REPORT, **RABBITMQ_PAYMENT)
