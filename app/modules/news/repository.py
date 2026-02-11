# DB操作
from typing import Sequence

from sqlalchemy import desc, func, select, update
from sqlalchemy.engine import CursorResult
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


class NewsRepository:
    """新闻相关"""

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

    @staticmethod
    async def get_news_by_id(db: AsyncSession, news_id: int):
        """根据新闻id查数据"""
        stmt = select(News).where(News.id == news_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def increase_news_views(db: AsyncSession, news_id: int):
        """新闻的浏览量 +1"""
        stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
        result = await db.execute(stmt)

        # 处理未知异常导致where到数据但是update异常，未更新数据
        assert isinstance(result, CursorResult)
        return result.rowcount > 0

    @staticmethod
    async def get_related_news(
        db: AsyncSession, news_id: int, category_id: int, limit: int = 5
    ):
        """
        查询相关文章
        阅览量+发布时间倒序
        """
        stmt = (
            select(News)
            .where(News.category_id == category_id, News.id != news_id)
            .order_by(News.views.desc(), News.publish_time.desc())
            .limit(limit)
        )
        result = await db.execute(stmt)

        return result.scalars().all()
