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


class FavoriteListItemResponse(BaseModel):
    """
    收藏列表
    新闻Schema
    """

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    title: str
    description: str
    image: str
    author: str
    views: int
    publish_time: datetime = Field(serialization_alias="publishTime")
    category_id: int
    favorite_id: int = Field(serialization_alias="favoriateId")
    favorite_time: datetime = Field(serialization_alias="favoriteTime")

    @field_serializer("publish_time")
    def serialize_datetimes(self, value: datetime | None) -> None | str:
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")
