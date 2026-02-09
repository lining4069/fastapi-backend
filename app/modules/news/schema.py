# Pydantic DTO
from app.common.base import BaseOutputSchema


class CategotyOutSchema(BaseOutputSchema):
    """新闻分类输出"""

    id: int
    name: str
    sort_order: int
