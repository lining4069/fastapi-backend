# Pydantic DTO
from datetime import datetime
from typing import Optional

from pydantic import Field, field_serializer

from app.common.base import BaseSchema


class CategotyOutSchema(BaseSchema):
    """新闻分类输出"""

    id: int
    name: str
    sort_order: int


class NewsSchema(BaseSchema):
    """新闻"""

    id: int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    views: int
    publish_time: datetime

    @field_serializer("publish_time")
    def serialize_publish_time(self, value: datetime | None):
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")


class NewsDetailSchema(BaseSchema):
    id: int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    views: int
    publish_time: datetime
    related_news: list[NewsSchema] = Field([], alias="relatedNews")
