# Settings/env
import os
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

APP_BASE_DIR = Path(__file__).resolve().parent.parent

ENVFILE_PATH_BY_ENV = os.path.join(APP_BASE_DIR, "env", f".env.{os.getenv('ENV')}")


class Settings(BaseSettings):
    # FastAPI 层面DEBUG开关
    DEBUG: bool = True
    # 数据库连接信息
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    # 数据库egine/连接池
    DB_ECHO: bool
    DB_POOL_SIZE: int
    DB_MAX_OVERFLOW: int
    DB_POOL_TIMEOUT: int
    DB_POOL_RECYCLE: int
    # CORS 前端Configs
    ALLOW_ORIGINS: List[str]
    ALLOW_CREDENTIALS: bool
    ALLOW_METHODS: List[str]
    ALLOW_HEADERS: List[str]
    # Token 有效期
    TOKEN_VALID_DURATION_DAYS: int

    model_config = SettingsConfigDict(
        env_file=ENVFILE_PATH_BY_ENV, env_file_encoding="utf-8"
    )


settings = Settings()  # type: ignore
