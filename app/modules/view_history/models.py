from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.common.base import ORMBase
from app.modules.news.model import News
from app.modules.users.models import User


class ViewHistory(ORMBase):
    """
    浏览历史表ORM模型
    """

    __tablename__ = "history"

    # 创建索引
    __table_args__ = (
        Index("fk_history_user_idx", "user_id"),
        Index("fk_history_news_idx", "news_id"),
        Index("idx_view_time", "view_time"),
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment="历史ID"
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(User.id), nullable=False, comment="用户ID"
    )
    news_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(News.id), nullable=False, comment="新闻ID"
    )
    view_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, comment="浏览时间"
    )

    def __repr__(self):
        return f"<History(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, view_time={self.view_time})>"
