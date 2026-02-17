from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.auth import get_current_user
from app.common.responses import APIResponse
from app.core.database import get_db
from app.core.logging import get_logger
from app.modules.users.models import User
from app.modules.view_history.schema import ViewHistoryAddRequest, ViewRecordReponse
from app.modules.view_history.service import ViewHistoryService

logger = get_logger(__name__)

router = APIRouter()


@router.post("/add", response_model=APIResponse[ViewRecordReponse])
async def add_view_history(
    data: ViewHistoryAddRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """增加浏览记录"""
    logger.info("增加浏览记录接口 '/add' 被访问")
    result = await ViewHistoryService.add_view_history(db, user, data)
    return APIResponse.success(data=result, message="增加浏览历史成功")
