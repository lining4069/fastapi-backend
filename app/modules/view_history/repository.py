from datetime import datetime
from typing import Sequence, Tuple

from sqlalchemy import func, select
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.news.model import News
from app.modules.view_history.models import ViewHistory


class ViewHisttoryRepository:
    @staticmethod
    async def add_view_record(
        db: AsyncSession, user_id: int, news_id: int
    ) -> ViewHistory:
        """增加浏览历史记录"""
        favorite = ViewHistory(user_id=user_id, news_id=news_id)
        db.add(favorite)
        await db.commit()
        await db.refresh(favorite)

        return favorite

    @staticmethod
    async def get_user_viewed_news(
        db: AsyncSession, user_id: int, offset: int, limit: int
    ) -> Sequence[Row[Tuple[News, datetime]]]:
        """获取用户浏览历史新闻列表"""
        stmt = (
            select(News, ViewHistory.view_time)
            .join(ViewHistory, News.id == ViewHistory.news_id)
            .where(ViewHistory.user_id == user_id)
            .order_by(ViewHistory.view_time.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await db.execute(stmt)

        return result.unique().all()

    @staticmethod
    async def get_user_view_count(db: AsyncSession, user_id: int) -> int:
        """获取用户浏览新闻总数"""
        stmt_total = select(func.count(ViewHistory.id)).where(
            ViewHistory.user_id == user_id
        )
        total = await db.execute(stmt_total)

        return total.scalar_one()
