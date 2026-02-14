from typing import Generic, Sequence, TypeVar

from fastapi import Query
from pydantic import BaseModel, ConfigDict


class PageParams:
    """分页参数依赖项"""

    def __init__(self, page: int, limit: int):
        self.page = page
        self.limit = limit
        self.offset = (page - 1) * limit

    def calc_has_more(self, total: int) -> bool:
        return self.page * self.limit < total


def get_page_params(
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(10, alias="pageSize", ge=1, le=100, description="每页数量"),
) -> PageParams:
    """获取分页参数"""
    return PageParams(page=page, limit=limit)


T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    list: Sequence[T]
    total: int
    hasMore: bool

    model_config = ConfigDict(from_attributes=True)
