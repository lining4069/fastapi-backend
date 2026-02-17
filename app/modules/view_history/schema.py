from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


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
