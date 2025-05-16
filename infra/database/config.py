from pydantic_settings import BaseSettings

from tg_bot.config import dotenv_path


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_TIMEZONE: str
    DATABASE_INIT_SQL_FILE_PATH: str

    class Config:
        env_file = dotenv_path
        extra = "allow"


postgresql_settings = Settings()
