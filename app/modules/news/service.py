# 业务逻辑
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.pagination import Page, PageParams
from app.modules.news.repository import CategoryRepository


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

    @staticmethod
    async def get_news_list(db: AsyncSession, category_id, params: PageParams):
        """获取指定新闻类别下新闻列表"""
        data = await CategoryRepository.get_news_list(
            db, category_id, params.offset, params.limit
        )
        total = await CategoryRepository.get_news_count(db, category_id)
        hasMore = params.calc_has_more(total)

        return Page(list=data, total=total, hasMore=hasMore)
