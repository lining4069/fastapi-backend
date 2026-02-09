from typing import Generic, Sequence, TypeVar

from fastapi import status
from pydantic import BaseModel, ConfigDict, Field


class PageParams(BaseModel):
    """分页参数依赖项"""

    page: int = Field(1, ge=1)  # 页数
    limit: int = Field(10, ge=1, le=100)  #  一页显示多少条

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    """页"""

    code: str = str(
        status.HTTP_200_OK,
    )
    message: str = "Success"
    data: Sequence[T]
    page: int
    limit: int
    total: int

    model_config = ConfigDict(from_attributes=True)
