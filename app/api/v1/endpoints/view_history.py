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


@router.delete("/delete/{history_id}")
async def delete_view_record(
    history_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """删除单条浏览记录"""
    logger.info("删除单条浏览记录接口 '/delete' 被访问")
    result = await ViewHistoryService.remove_news_record(db, history_id)
    return APIResponse.success(data=result, message="删除浏览记录成功")


@router.delete("/clear", response_model=APIResponse)
async def clear_favorite_news(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """清除用户的新闻收藏"""
    logger.info("清除用户浏览历史接口 '/clear' 被访问")
    clear_count = await ViewHistoryService.clear_view_history(db, user)
    return APIResponse.success(
        data=None, message=f"清空浏览历史成功,共计清除用户{clear_count}条记录。"
    )
