from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
