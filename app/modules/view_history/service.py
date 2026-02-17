from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import User
from app.modules.view_history.repository import ViewHisttoryRepository
from app.modules.view_history.schema import ViewHistoryAddRequest, ViewRecordReponse


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
