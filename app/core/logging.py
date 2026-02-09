# app/core/logging.py
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Optional

from app.core.config import APP_BASE_DIR

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(
    *,
    level: int = logging.INFO,
    log_dir: str = f"{APP_BASE_DIR}/logs",
    log_file: str = "app.log",
    when: str = "midnight",  # 按天切割
    interval: int = 1,
    backup_count: int = 14,  # 保留 14 天
) -> None:
    """
    初始化全局 logging 配置（只调用一次）
    """

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # 防止重复添加 handler（uvicorn --reload 时非常关键）
    if root_logger.handlers:
        return

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    # stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # file
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    file_handler = TimedRotatingFileHandler(
        filename=log_path / log_file,
        when=when,
        interval=interval,
        backupCount=backup_count,
        encoding="utf-8",
        utc=False,  # 用本地时间，便于排查
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # # 按照日志文件大小切割
    # from logging.handlers import RotatingFileHandler

    # file_handler = RotatingFileHandler(
    #     filename=log_path / log_file,
    #     maxBytes=100 * 1024 * 1024,  # 100MB
    #     backupCount=10,
    #     encoding="utf-8",
    # )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(name)
