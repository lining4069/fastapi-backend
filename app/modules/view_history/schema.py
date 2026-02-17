from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class ViewHistoryAddRequest(BaseModel):
    """增加浏览记录请求体Model"""

    news_id: int = Field(..., validation_alias="newsId", description="新闻ID")


class ViewRecordReponse(BaseModel):
    """浏览记录 Output Schema"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int = Field(serialization_alias="userId", description="用户ID")
    news_id: int = Field(serialization_alias="newsId", description="新闻ID")
    view_time: datetime = Field(serialization_alias="viewTime", description="浏览时间")


class ViewHisttoryItemResponse(BaseModel):
    """获取用户新闻浏览历史列表 新闻单元 Schema"""

    model_config = ConfigDict(from_attributes=True)

    history_id: int = Field(serialization_alias="id")
    view_time: datetime = Field(serialization_alias="viewTime")

    title: str
    description: str
    image: str
    author: str
    views: int
    publish_time: datetime = Field(serialization_alias="publishTime")
    category_id: int

    @field_serializer("publish_time", "view_time")
    def serialize_datetimes(self, value: datetime | None) -> None | str:
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")
