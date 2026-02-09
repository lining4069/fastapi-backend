# DB操作
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.news.model import Category


class CategoryRepository:
    """新闻类别"""

    @staticmethod
    async def get_all_categoty_paginated(
        db: AsyncSession, offset: int, limit: int
    ) -> tuple[Sequence[Category], int]:
        stmt = select(Category).order_by(Category.sort_order)
        total_stmt = select(func.count()).select_from(Category)
        data = await db.execute(stmt.offset(offset).limit(limit))
        total = await db.execute(total_stmt)

        return data.scalars().all(), total.scalar_one()

    @staticmethod
    async def get_all_categoty(
        db: AsyncSession, offset: int, limit: int
    ) -> Sequence[Category]:
        stmt = select(Category).order_by(Category.sort_order)
        data = await db.execute(stmt.offset(offset).limit(limit))

        return data.scalars().all()
