from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from app.api.v1.api import api_router
from app.common.exceptions import http_exception_handler
from app.core.logging import setup_logging


def setup() -> FastAPI:
    # 初始化全局日志器
    setup_logging()
    # 声明fastapi app
    app = FastAPI(
        title="FastAPI Backend",
        version="1.0.0",
    )
    # 导入路由
    app.include_router(api_router, prefix="/api/v1")
    # 注册exception处理
    app.add_exception_handler(HTTPException, http_exception_handler)

    return app


app = setup()
