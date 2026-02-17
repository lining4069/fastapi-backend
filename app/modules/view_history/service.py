from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import DatabaseOperationException
from app.common.pagination import Page, PageParams
from app.modules.users.models import User
from app.modules.view_history.repository import ViewHisttoryRepository
from app.modules.view_history.schema import (
    ViewHistoryAddRequest,
    ViewHisttoryItemResponse,
    ViewRecordReponse,
)


class ViewHistoryService:
    @staticmethod
    async def add_view_history(
        db: AsyncSession, user: User, data: ViewHistoryAddRequest
    ) -> ViewRecordReponse:
        """增加浏览历史"""
        view_record = await ViewHisttoryRepository.add_view_record(
            db, user.id, data.news_id
        )
        return ViewRecordReponse.model_validate(view_record)

    @staticmethod
    async def get_view_history(db: AsyncSession, user: User, params: PageParams):
        """获取浏览历史"""
        result = await ViewHisttoryRepository.get_user_viewed_news(
            db, user.id, params.offset, params.limit
        )
        data = [
            ViewHisttoryItemResponse(
                history_id=history_id,
                view_time=view_time,
                **news.__dict__,
            )
            for news, history_id, view_time in result
        ]
        total = await ViewHisttoryRepository.get_user_view_count(db, user.id)
        hasMore = params.calc_has_more(total)

        return Page(list=data, total=total, hasMore=hasMore)

    @staticmethod
    async def remove_news_record(db: AsyncSession, history_id: int) -> None:
        """删除新闻浏览历史记录"""
        delete_rowcount = await ViewHisttoryRepository.remove_vied_record(
            db, history_id
        )
        if delete_rowcount == 0:
            raise DatabaseOperationException(
                "用户收藏", f"浏览记录ID: {history_id}", "删除"
            )
        return None

    @staticmethod
    async def clear_view_history(db: AsyncSession, user: User) -> int:
        """清空用户浏览历史"""
        return await ViewHisttoryRepository.delete_view_history(db, user.id)
