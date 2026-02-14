from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.common.exception_handlers import register_exception_handlers
from app.core.config import settings
from app.core.logging import setup_logging


def setup() -> FastAPI:
    # 初始化全局日志器
    setup_logging()
    # 声明fastapi app
    app = FastAPI(
        title="FastAPI Backend",
        version="1.0.0",
    )
    # 添加CORS 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,  # 允许访问的源
        allow_credentials=settings.ALLOW_CREDENTIALS,  # 允许携带cookies
        allow_methods=settings.ALLOW_METHODS,  # 允许所有请求方式
        allow_headers=settings.ALLOW_HEADERS,  # 允许所有请求头
    )
    # 导入路由
    app.include_router(api_router, prefix="/api")
    # 注册exception处理
    register_exception_handlers(app)

    return app


app = setup()
