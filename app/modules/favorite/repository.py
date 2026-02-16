from sqlalchemy import delete, func, select
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.favorite.models import Favorite
from app.modules.news.model import News


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

    @staticmethod
    async def remove_favorite(db: AsyncSession, user_id: int, news_id: int) -> int:
        """删除收藏记录"""
        stmt = delete(Favorite).where(
            Favorite.user_id == user_id, Favorite.news_id == news_id
        )
        result = await db.execute(stmt)

        await db.commit()

        assert isinstance(result, CursorResult)
        return result.rowcount

    @staticmethod
    async def get_favorite_news(
        db: AsyncSession, user_id: int, offset: int, limit: int
    ):
        """根据offset+limit获取收藏的新闻列表"""
        stmt = (
            select(
                News,
                Favorite.id.label("favorite_id"),
                Favorite.created_at.label("favorite_time"),
            )
            .join(Favorite, News.id == Favorite.news_id)
            .where(Favorite.user_id == user_id)
            .order_by(Favorite.created_at.desc())
            .offset(offset=offset)
            .limit(limit)
        )
        result = await db.execute(stmt)

        return result.all()

    @staticmethod
    async def get_user_favorited_count(db: AsyncSession, user_id: int) -> int:
        """获取用户收藏总数"""
        stmt_total = select(func.count(Favorite.id)).where(Favorite.user_id == user_id)
        total = await db.execute(stmt_total)

        return total.scalar_one()

    @staticmethod
    async def delete_user_favorite(db: AsyncSession, user_id: int) -> int:
        """清空用户收藏"""
        stmt = delete(Favorite).where(Favorite.user_id == user_id)
        result = await db.execute(stmt)

        await db.commit()

        assert isinstance(result, CursorResult)
        return result.rowcount
