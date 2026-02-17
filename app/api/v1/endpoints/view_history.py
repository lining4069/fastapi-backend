from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.auth import get_current_user
from app.common.pagination import Page, PageParams, get_page_params
from app.common.responses import APIResponse
from app.core.database import get_db
from app.core.logging import get_logger
from app.modules.users.models import User
from app.modules.view_history.schema import (
    ViewHistoryAddRequest,
    ViewHisttoryItemResponse,
    ViewRecordReponse,
)
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


@router.get("/list", response_model=APIResponse[Page[ViewHisttoryItemResponse]])
async def get_view_history(
    params: PageParams = Depends(get_page_params),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取浏览历史"""
    logger.info("获取用户新闻收藏列表接口 '/list' 被访问")
    result = await ViewHistoryService.get_view_history(db, user, params)
    return APIResponse.success(data=result, message="获取用户浏览历史列表成功")
