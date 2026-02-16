from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.favorite.models import Favorite
from app.modules.favorite.repository import FavoriteRepository
from app.modules.favorite.schema import FavoriteAddRequest
from app.modules.users.models import User


class FavoriteService:
    @staticmethod
    async def check_news_favorite_state(
        db: AsyncSession,
        user: User,
        news_id: int,
    ) -> bool:
        """检查新闻收藏状态"""
        result = await FavoriteRepository.is_news_favorite(db, user.id, news_id)
        return True if result else False

    @staticmethod
    async def add_news_to_favorite(
        db: AsyncSession,
        user: User,
        data: FavoriteAddRequest,
    ) -> Favorite:
        """收藏新闻"""
        return await FavoriteRepository.add_favorite(db, user.id, data.news_id)
