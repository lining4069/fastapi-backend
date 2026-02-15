from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.common.base import BaseSchema


class UserRequest(BaseModel):
    """用户注册"""

    username: str
    password: str


class GenderEnum(str, Enum):
    """性别枚举（与数据库对应）"""

    male = "male"
    female = "female"
    unknown = "unknown"


class UserInfoBase(BaseModel):
    """基础模型,包含所有公共字段"""

    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(
        "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
        max_length=255,
        description="头像URL",
    )
    gender: GenderEnum = Field(GenderEnum.unknown, description="性别")
    bio: Optional[str] = Field(
        "这个人很懒，什么都没留下", max_length=500, description="个人简介"
    )


class UserInfoResponse(UserInfoBase, BaseSchema):
    """用户信息响应"""

    id: int
    username: str = Field(..., min_length=3, max_length=50, description="用户名")


class UserAuthResponse(BaseModel):
    """注册返回响应"""

    token: str
    userInfo: UserInfoResponse

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class UserUpdateRequest(BaseModel):
    """用户更新请求请求体"""

    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
