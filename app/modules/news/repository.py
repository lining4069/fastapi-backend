# DB操作
from typing import Sequence

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.news.model import Category, News


class CategoryRepository:
    """新闻类别"""

    @staticmethod
    async def get_all_categoty_paginated(
        db: AsyncSession, offset: int, limit: int
    ) -> tuple[Sequence[Category], int]:
        """获取新闻类别数据以及总数"""
        stmt = select(Category).order_by(Category.sort_order)
        data = await db.execute(stmt.offset(offset).limit(limit))

        total_stmt = select(func.count()).select_from(Category)
        total = await db.execute(total_stmt)

        return data.scalars().all(), total.scalar_one()

    @staticmethod
    async def get_all_category(
        db: AsyncSession, offset: int, limit: int
    ) -> Sequence[Category]:
        """获取所有新闻类别"""
        stmt = select(Category).order_by(Category.sort_order)
        data = await db.execute(stmt.offset(offset).limit(limit))

        return data.scalars().all()

    @staticmethod
    async def get_news_list(
        db: AsyncSession, category_id: int, offset: int, limit: int
    ) -> Sequence[News]:
        """分页的获得指定新闻列表下的新闻内容"""
        stmt_data = (
            select(News)
            .where(News.category_id == category_id)
            .order_by(desc(News.publish_time))
            .offset(offset)
            .limit(limit)
        )
        data = await db.execute(stmt_data)

        return data.scalars().all()

    @staticmethod
    async def get_news_count(db: AsyncSession, category_id: int) -> int:
        """获取指定新闻类别下的新闻总数"""
        stmt_total = select(func.count(News.id)).where(News.category_id == category_id)
        total = await db.execute(stmt_total)

        return total.scalar_one()
