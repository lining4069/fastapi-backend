# SQLAlchemy ORM
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.base import Base


class Category(Base):
    __tablename__ = "news_category"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="ID")
    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, comment="分类名称"
    )
    sort_order: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False, comment="排序"
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id},name={self.name},sort_order:{self.sort_order})>"
