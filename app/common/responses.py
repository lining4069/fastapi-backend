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
    return APIResponse(code=status.HTTP_200_OK, message=message, data=data)
