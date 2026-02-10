from typing import Generic, Optional, TypeVar

from fastapi import status
from pydantic import BaseModel

# 通用响应模型
T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = None


# 成功响应
def success(data=None, message: str = "Success"):
    """路由处理函数 设置了response_model=pydantic Model"""
    return APIResponse(code=status.HTTP_200_OK, message=message, data=data)


def success_without_schema(data=None, message: str = "Success"):
    """
    路由处理函数 不设置 response_model=pydantic Model
    只是简单
    """
    return {"code": status.HTTP_200_OK, "message": message, "data": data}
