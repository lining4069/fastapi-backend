from sqlalchemy.ext.asyncio import AsyncSession

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
