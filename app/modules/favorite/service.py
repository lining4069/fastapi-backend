from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import DatabaseOperationException
from app.modules.favorite.models import Favorite
from app.modules.favorite.repository import FavoriteRepository
from app.modules.favorite.schema import FavoriteAddRequest, FavoriteCheckResponse
from app.modules.users.models import User


class FavoriteService:
    @staticmethod
    async def check_news_favorite_state(
        db: AsyncSession,
        user: User,
        news_id: int,
    ) -> FavoriteCheckResponse:
        """检查新闻收藏状态"""
        result = await FavoriteRepository.is_news_favorite(db, user.id, news_id)
        is_favorite = True if result else False
        return FavoriteCheckResponse(is_favorite=is_favorite)

    @staticmethod
    async def add_news_to_favorite(
        db: AsyncSession,
        user: User,
        data: FavoriteAddRequest,
    ) -> Favorite:
        """收藏新闻"""
        return await FavoriteRepository.add_favorite(db, user.id, data.news_id)

    @staticmethod
    async def remove_news_favorite(db: AsyncSession, user: User, news_id: int) -> None:
        delete_rowcount = await FavoriteRepository.remove_favorite(db, user.id, news_id)
        if delete_rowcount == 0:
            raise DatabaseOperationException(
                "用户收藏", {"user_id": user.id, "news_id": news_id}, "删除"
            )
