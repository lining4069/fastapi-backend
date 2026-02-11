# 业务逻辑
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import BusinessException
from app.common.pagination import Page, PageParams
from app.core.logging import get_logger
from app.modules.news.repository import CategoryRepository, NewsRepository

logger = get_logger(__name__)


class CategoryService:
    """新闻分类服务"""

    @staticmethod
    async def get_category_paginated(db: AsyncSession, params: PageParams):
        data, total = await CategoryRepository.get_all_categoty_paginated(
            db, params.offset, params.limit
        )
        hasMore = params.offset + params.limit < total
        return Page(list=data, total=total, hasMore=hasMore)

    @staticmethod
    async def get_category(db: AsyncSession, params: PageParams):
        """获取所有新闻类别"""
        return await CategoryRepository.get_all_category(
            db, params.offset, params.limit
        )


class NewsService:
    """新闻相关服务"""

    @staticmethod
    async def get_news_list(db: AsyncSession, category_id, params: PageParams):
        """获取指定新闻类别下新闻列表"""
        data = await NewsRepository.get_news_list(
            db, category_id, params.offset, params.limit
        )
        total = await NewsRepository.get_news_count(db, category_id)
        hasMore = params.calc_has_more(total)

        return Page(list=data, total=total, hasMore=hasMore)

    @staticmethod
    async def view_news_detail(db: AsyncSession, news_id: int):
        """根据新闻ID 进入新闻详情"""
        # 获取新闻详情
        news_detail = await NewsRepository.get_news_by_id(db, news_id)
        if news_detail is None:
            return None, None
        # 浏览量+1
        updated = await NewsRepository.increase_news_views(db, news_id)
        if not updated:
            raise BusinessException(
                f"updated table `news`  field `views` where `id={news_id}` fail !"
            )
        await db.refresh(news_detail)
        # 相关新闻
        related_news = await NewsRepository.get_related_news(
            db, news_id, news_detail.category_id
        )

        return news_detail, related_news
