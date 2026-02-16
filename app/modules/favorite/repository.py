from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.favorite.models import Favorite


class FavoriteRepository:
    @staticmethod
    async def is_news_favorite(
        db: AsyncSession, user_id: int, news_id: int
    ) -> Favorite | None:
        """查询新闻是否被当前用户收藏"""
        stmt = select(Favorite).where(
            Favorite.user_id == user_id, Favorite.news_id == news_id
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    async def add_favorite(db: AsyncSession, user_id: int, news_id: int) -> Favorite:
        """增加收藏记录"""
        favorite = Favorite(user_id=user_id, news_id=news_id)
        db.add(favorite)
        await db.commit()
        await db.refresh(favorite)

        return favorite
