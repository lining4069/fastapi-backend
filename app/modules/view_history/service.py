from sqlalchemy.ext.asyncio import AsyncSession

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
            ViewHisttoryItemResponse(**news.__dict__, view_time=view_time)
            for news, view_time in result
        ]
        total = await ViewHisttoryRepository.get_user_view_count(db, user.id)
        hasMore = params.calc_has_more(total)

        return Page(list=data, total=total, hasMore=hasMore)
