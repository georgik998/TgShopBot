from pydantic_settings import BaseSettings

from tg_bot.config import dotenv_path


class CryptobotApiSettings(BaseSettings):
    CRYPTOBOT_API_TOKEN: str

    class Config:
        env_file = dotenv_path
        extra = "allow"


cryptobot_api_settings = CryptobotApiSettings()
