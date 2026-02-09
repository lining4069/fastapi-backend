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
        return Page(data=data, page=params.page, limit=params.limit, total=total)

    @staticmethod
    async def get_category(db: AsyncSession, skip: int = 0, limit: int = 100):
        return await CategoryRepository.get_all_categoty(db, skip, limit)
