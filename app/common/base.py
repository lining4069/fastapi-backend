# 跨模块通用代码
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    # server_default 由数据库服务器生成，ORM只是声明，不参与计算。default是由sqlalchemy在session.add()添值，是应用服务器时间
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        comment="创建时间",
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    )


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    updated_at: datetime

    @field_serializer(
        "created_at",
        "updated_at",
    )
    def serialize_datetime(self, value: datetime | None):
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")
