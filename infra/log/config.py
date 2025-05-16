from pydantic_settings import BaseSettings

from tg_bot.config import dotenv_path


class LoggerSettings(BaseSettings):
    LOG_FILE_PATH: str
    LOGGER_NAME: str

    class Config:
        env_file = dotenv_path
        extra = "allow"


logger_settings = LoggerSettings()
