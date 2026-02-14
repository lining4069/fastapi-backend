from typing import Generic, Optional, TypeVar

from fastapi import status
from pydantic import BaseModel, ConfigDict

# 通用响应模型
T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    code: int = status.HTTP_200_OK
    message: str = "Success"
    data: Optional[T] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def success(cls, data: T = None, message: str = "Success"):
        return cls(code=status.HTTP_200_OK, message=message, data=data)

    @classmethod
    def fail(
        cls, code: int = status.HTTP_400_BAD_REQUEST, message: str = "Fail", data=None
    ):
        return cls(code=code, message=message, data=data)
