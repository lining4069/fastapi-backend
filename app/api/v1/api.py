# 汇总api
from fastapi import APIRouter

from app.api.v1.endpoints import news, users

api_router = APIRouter()

# tags:z在接口文档中的分组名
api_router.include_router(news.router, prefix="/news", tags=["News"])
api_router.include_router(users.router, prefix="/user", tags=["Users"])
