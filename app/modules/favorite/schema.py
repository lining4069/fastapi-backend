from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class FavoriteCheckResponse(BaseModel):
    """检查新闻收藏情况响应"""

    model_config = ConfigDict(populate_by_name=True)

    is_favorite: bool = Field(
        ..., serialization_alias="isFavorite", description="是否收藏"
    )


class FavoriteAddRequest(BaseModel):
    """收藏请求体"""

    news_id: int = Field(..., alias="newsId")


class FavoriteInfoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    news_id: int
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime | None) -> None | str:
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")
