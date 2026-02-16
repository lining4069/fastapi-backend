from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import DatabaseOperationException
from app.common.pagination import Page, PageParams
from app.modules.favorite.repository import FavoriteRepository
from app.modules.favorite.schema import (
    FavoriteAddRequest,
    FavoriteCheckResponse,
    FavoriteInfoResponse,
    FavoriteListItemResponse,
)
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
    ) -> FavoriteInfoResponse:
        """收藏新闻"""
        result = await FavoriteRepository.add_favorite(db, user.id, data.news_id)
        return FavoriteInfoResponse.model_validate(result)

    @staticmethod
    async def remove_news_favorite(db: AsyncSession, user: User, news_id: int) -> None:
        delete_rowcount = await FavoriteRepository.remove_favorite(db, user.id, news_id)
        if delete_rowcount == 0:
            raise DatabaseOperationException(
                "用户收藏", {"user_id": user.id, "news_id": news_id}, "删除"
            )

    @staticmethod
    async def get_favorite_news(
        db: AsyncSession, user: User, params: PageParams
    ) -> Page[FavoriteListItemResponse]:
        """获取收藏列表"""
        result = await FavoriteRepository.get_favorite_news(
            db, user.id, params.offset, params.limit
        )
        data = [
            FavoriteListItemResponse(
                **news.__dict__, favorite_id=favorite_id, favorite_time=favorite_time
            )
            for news, favorite_id, favorite_time in result
        ]
        total = await FavoriteRepository.get_user_favorited_count(db, user.id)
        hasMore = params.calc_has_more(total)
        return Page(list=data, total=total, hasMore=hasMore)
