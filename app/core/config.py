# Settings/env
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

APP_BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # 数据库配置信息
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str

    model_config = SettingsConfigDict(
        env_file=f"{APP_BASE_DIR}/.env", env_file_encoding="utf-8"
    )


settings = Settings()  # type: ignore
